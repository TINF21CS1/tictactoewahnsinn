import json, sys, time, socket, pytest
from unittest.mock import patch, MagicMock
sys.path.append("..")
sys.path.append("../tictactoewahnsinn")
from networking import Network

@pytest.fixture
def mock_socket():
    with patch('socket.socket') as mock:
        yield mock

@pytest.fixture
def network_instance():
    return Network(id="test_id", host="localhost", port=5000, discover_timeout=5.0, connection_timeout=10.0)

def test_initialization(network_instance):
    # Asserting initialization parameters are correctly assigned
    assert network_instance.id == "test_id"
    assert network_instance.host == "localhost"
    assert network_instance.port == 5000

def test_init_broadcast_socket_success(mock_socket, network_instance):
    # Asserting successful initialization of the broadcast socket
    network_instance.init_broadcast_socket()
    mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    mock_socket.return_value.setsockopt.assert_called()
    mock_socket.return_value.bind.assert_called_with(('', network_instance.port))

def test_init_connection_socket_success(mock_socket, network_instance):
    # Asserting successful initialization of the connection socket
    network_instance.init_connection_socket()
    mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
    mock_socket.return_value.setsockopt.assert_called()
    mock_socket.return_value.bind.assert_called_with((network_instance.host, network_instance.port + 1))

def test_init_peer_connection_success(network_instance):
    # Asserting a successful connection with another peer
    addr = ("localhost", 5000)
    with patch('socket.create_connection', return_value=MagicMock()) as mock_create_connection, \
         patch('logging.info') as mock_logging_info:
        result = network_instance.init_peer_connection(addr)
        mock_create_connection.assert_called_once_with(addr)
        assert result is not None
        mock_logging_info.assert_called_once_with(f"[Peer-Verbindung] Verbindung mit {addr[0]}:{addr[1]} erfolgreich")

def test_init_peer_connection_reuse(network_instance):
    # Testing reusing an existing peer connection without creating a new one
    network_instance.peer_connection = MagicMock()
    addr = ("localhost", 5000)
    result = network_instance.init_peer_connection(addr)
    assert result == network_instance.peer_connection
    with patch('socket.create_connection') as mock_create_connection:
        network_instance.init_peer_connection(addr)
        mock_create_connection.assert_not_called()

def test_init_peer_connection_failure(network_instance):
    # Testing peer connection failure handling
    addr = ("localhost", 5000)
    with patch('socket.create_connection', side_effect=Exception("Connection failed")), \
         patch('logging.error') as mock_logging_error:
        result = network_instance.init_peer_connection(addr)
        assert result is None
        mock_logging_error.assert_called_once()

def test_get_potentialPeers_returns_correct_list(network_instance):
    # Testing if the correct list of potential peers is returned
    network_instance.potential_peers = ["peer1", "peer2", "peer3"]
    result = network_instance.get_potentialPeers()
    assert result == ["peer1", "peer2", "peer3"], "The returned list of potential peers is incorrect."

def test_get_potentialPeers_returns_list_copy(network_instance):
    # Testing if a copy of the potential peers list is returned
    network_instance.potential_peers = ["peer1", "peer2", "peer3"]
    result = network_instance.get_potentialPeers()
    result.append("peer4")
    assert network_instance.potential_peers == ["peer1", "peer2", "peer3"], "The method should return a copy of the potential peers list."

def test_get_currentPeer_with_valid_connection(network_instance):
    # Testing retrieval of current peer address when the connection is valid
    mock_connection = MagicMock()
    mock_connection.getpeername.return_value = ("localhost", 5000)
    network_instance.peer_connection = mock_connection
    assert network_instance.get_currentPeer() == ("localhost", 5000), "The method should return the correct peer address."

def test_get_currentPeer_with_error(network_instance):
    # Testing error handling when retrieving current peer address fails
    mock_connection = MagicMock()
    mock_connection.getpeername.side_effect = socket.error
    network_instance.peer_connection = mock_connection
    with patch('socket.error', new=Exception):
        assert network_instance.get_currentPeer() is None, "The method should handle socket.error and return None."

def test_get_currentPeer_no_connection(network_instance):
    # Testing behavior when there is no current peer connection
    network_instance.peer_connection = None
    assert network_instance.get_currentPeer() is None, "The method should return None when no peer connection exists."

def test_connect_peer_client_success(network_instance):
    # Testing successful peer client connection
    addr = ("127.0.0.1", 5000)
    with patch('networking.logging', MagicMock()) as mock_logging:
        network_instance.init_peer_connection = MagicMock(return_value=MagicMock())
        network_instance.handle_connection = MagicMock()

        assert network_instance.connect_peer_client(addr) is True, "connect_peer_client should return True when the connection is successfully established."
        mock_logging.info.assert_called()

def test_connect_peer_client_failure(network_instance):
    # Testing failure in peer client connection
    addr = ("127.0.0.1", 5000)
    with patch('networking.socket', MagicMock()) as mock_socket, \
        patch('networking.logging', MagicMock()) as mock_logging:
        mock_socket.error = socket.error
        network_instance.init_peer_connection = MagicMock(side_effect=socket.error("Connection failed"))

        assert network_instance.connect_peer_client(addr) is False, "connect_peer_client should return False when the connection fails to establish."
        mock_logging.error.assert_called()

def test_connect_peer_server(network_instance):
    # Asserting the server setup and connection acceptance process
    with patch('networking.socket') as mock_socket:
        mock_socket.error = socket.error
        with patch('networking.logging') as mock_logging:
            mock_server = MagicMock()
            mock_server.listen = MagicMock()
            mock_server.accept = MagicMock(return_value=(MagicMock(), ("localhost", 5001)))
            mock_server.create_server.return_value = MagicMock(__enter__=MagicMock(return_value=mock_server), __exit__=MagicMock())
            network_instance.init_connection_socket = MagicMock(return_value=MagicMock(__enter__=MagicMock(return_value=mock_server), __exit__=MagicMock()))
            network_instance.handle_connection = MagicMock()
            network_instance.shutdown_event.is_set = MagicMock(side_effect=[False, True])

            network_instance.connect_peer_server()

            mock_logging.info.assert_called_with("[Peer-Verbindung] Verbindung von ('{}', {}) akzeptiert" .format(network_instance.host, (network_instance.port + 1)))
            mock_server.accept.assert_called()

def test_send_data_success(network_instance):
    # Asserting successful data transmission
    addr = ("127.0.0.1", 5000)
    data_type, data_content, timestamp = "testType", "testData", 1708353493.2045512
    with patch.object(network_instance, 'init_peer_connection', MagicMock()) as mock_init_peer_connection, \
        patch('networking.logging', MagicMock()) as mock_logging:
        network_instance.send_data(addr, data_type, data_content, timestamp)
        expected_data = json.dumps({
            "id": network_instance.id,
            "type": data_type,
            "addr": (network_instance.host, network_instance.port),
            "time": timestamp,
            "data": data_content
        }).encode('utf-8')
        mock_init_peer_connection.return_value.__enter__.return_value.sendall.assert_called_with(expected_data), \
            "Expected sendall to be called with the correctly formatted data."
        mock_logging.info.assert_called()

def test_send_data_failure(network_instance):
    # Asserting handling of data transmission failure
    addr = ("127.0.0.1", 5000)
    with patch.object(network_instance, 'init_peer_connection', side_effect=socket.error("Test failure")), \
        patch('networking.logging', MagicMock()) as mock_logging:
        network_instance.send_data(addr, "type", "data")
        mock_logging.error.assert_called(), "Expected logging.error to be called on failure to transmit data due to a socket error."

def test_recv_data_success(network_instance):
    # Asserting successful data reception
    received_json = json.dumps({"key": "value"}).encode('utf-8')
    with patch.object(network_instance, 'init_peer_connection', MagicMock()) as mock_init, \
        patch('networking.logging', MagicMock()) as mock_logging:
        mock_init.return_value.__enter__.return_value.recv.return_value = received_json
        result = network_instance.recv_data()
        assert result == json.loads(received_json.decode('utf-8')), "Expected recv_data to return the correct data structure after receiving valid JSON."
        mock_logging.info.assert_called()

def test_recv_data_connection_closed(network_instance):
    # Asserting behavior when connection is closed before data reception
    with patch.object(network_instance, 'init_peer_connection', MagicMock()) as mock_init, \
        patch('networking.logging', MagicMock()) as mock_logging:
        mock_init.return_value.__enter__.return_value.recv.return_value = b''
        assert network_instance.recv_data() is None,  "Expected recv_data to return None when the connection is closed (empty byte string received)."
        mock_logging.info.assert_called()

def test_recv_data_failure(network_instance):
    # Asserting handling of data reception failure
    with patch.object(network_instance, 'init_peer_connection', MagicMock()) as mock_init, \
        patch('networking.logging', MagicMock()) as mock_logging:
        mock_init.return_value.__enter__.return_value.recv.side_effect = socket.error("Test error")
        assert network_instance.recv_data() is None, "Expected recv_data to return None when data reception fails due to a socket error."
        mock_logging.error.assert_called()

def test_send_paket_success(network_instance):
    # Asserting successful packet transmission
    addr = ("127.0.0.1", 5000)
    packet_type = "testType"
    data = "testData"
    with patch('networking.socket.socket') as mock_socket, \
        patch('networking.time.time', return_value=1234567890):
        network_instance.send_paket(addr, packet_type, data)
        expected_msg = json.dumps({
            "id": network_instance.id,
            "type": packet_type,
            "addr": (network_instance.host, network_instance.port),
            "time": 1234567890,
            "data": data
        }).encode('utf-8')
        mock_socket.return_value.__enter__.return_value.sendto.assert_called_once_with(expected_msg, (addr[0], network_instance.port))

def test_send_paket_failure(network_instance):
    # Asserting handling of packet transmission failure
    addr = ("127.0.0.1", 5000)
    packet_type = "testType"
    data = "testData"
    with patch('networking.socket.socket', MagicMock()) as mock_socket, \
         patch('networking.logging', MagicMock()) as mock_logging:
        mock_socket.return_value.__enter__.return_value.sendto.side_effect = socket.error("Test error")
        network_instance.send_paket(addr, packet_type, data)
        mock_logging.error.assert_called_once_with("[send-paket] Fehler bei der Übertragung: Test error"),  "Expected logging.error to be called once with a message indicating transmission error."

def test_add_peer_new(network_instance):
    # Asserting addition of a new peer to the list
    peer_info = ("peer_id", ("localhost", 5000))
    with patch('time.time', return_value=1234567890), \
         patch('logging.info') as mock_logging_info:
        network_instance.add_peer(peer_info)
        assert (peer_info, 1234567890) in network_instance.potential_peers, "New peer should be added to the potential peers list with the current timestamp."
        mock_logging_info.assert_called_with(f"[Peer-Verbindung] Neuer Peer hinzugefügt: {peer_info}")

def test_add_peer_existing(network_instance):
    # Asserting no duplicate addition of an existing peer
    peer_info = ("peer_id", ("localhost", 5000))
    network_instance.potential_peers.append((peer_info, time.time()))
    initial_length = len(network_instance.potential_peers)
    network_instance.add_peer(peer_info)
    assert len(network_instance.potential_peers) == initial_length,  "Adding an existing peer should not alter the length of the potential peers list."

def test_remove_peer_existing(network_instance):
    # Asserting removal of an existing peer from the list
    peer_info = ("peer_id", ("localhost", 5000))
    network_instance.potential_peers.append(peer_info)
    with patch('logging.info') as mock_logging_info:
        network_instance.remove_peer(peer_info)
        assert peer_info not in network_instance.potential_peers, "Existing peer should be removed from the potential peers list."
        mock_logging_info.assert_called_with(f"[Peer-Verbindung] Peer entfernt: {peer_info}")

def test_remove_peer_nonexistent(network_instance):
    # Asserting attempt to remove a non-existent peer does not alter the list
    peer_info = ("peer_id", ("localhost", 5000))
    initial_length = len(network_instance.potential_peers)
    network_instance.remove_peer(peer_info)
    assert len(network_instance.potential_peers) == initial_length, "Non-existent peer removal should not alter the list."

def test_remove_stale_peers(network_instance):
    # Asserting removal of stale peers based on timestamp
    current_time = 1234567890
    old_peer_time = current_time - 100 
    new_peer_time = current_time - 10
    network_instance.potential_peers = [
        (("old_peer", "addr1"), old_peer_time),
        (("new_peer", "addr2"), new_peer_time),
    ]

    with patch('networking.time.time', return_value=current_time), \
        patch('networking.time.sleep', MagicMock()) as mock_sleep, \
        patch.object(network_instance.shutdown_event, 'is_set', side_effect=[False, True]), \
        patch('networking.logging', MagicMock()) as mock_logging:
        network_instance.remove_stale_peers()

        assert network_instance.potential_peers == [(("new_peer", "addr2"), new_peer_time)], "Stale peers (based on timestamp) should be removed, leaving only recent peers."
        mock_logging.info.assert_called_with("[Potential Peers] [(('new_peer', 'addr2'), 1234567880)]")
        mock_sleep.assert_called_with(30)
