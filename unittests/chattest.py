import pytest, sys
from unittest.mock import patch
from chat import Chat

sys.path.append("..")
sys.path.append("../tictactoewahnsinn")

@pytest.fixture
def chat_instance():
    return Chat("player1")

@pytest.fixture
def network_mock():
    with patch("chat.Network") as mock:
        yield mock

def test_chat_initialization(chat_instance):
    # Asserting initialization parameters are correctly assigned
    assert chat_instance.id == "player1"

def test_receive_data_successful(chat_instance, network_mock):
    # Asserting data is correctly received
    expected_message = "Hello, World!"
    network_mock.recv_data.return_value = expected_message
    result = chat_instance.receiveData("player2")
    network_mock.recv_data.assert_called_once()
    assert result == expected_message

def test_receive_data_exception(chat_instance, network_mock, caplog):
    # Asserting exception is correctly thrown
    network_mock.recv_data.side_effect = Exception()
    result = chat_instance.receiveData("player2")
    network_mock.recv_data.assert_called_once()
    assert "Fehler beim Empfangen von Chat-Nachricht" in caplog.text
    assert "Player: player2" in caplog.text
    assert result == "Fehler"

def test_send_data_successful(chat_instance, network_mock, caplog):
    # Asserting data is correctly send
    expected_message = "Hello, World!"
    network_mock.send_data.return_value = True
    result = chat_instance.sendData(expected_message)
    network_mock.send_data.assert_called_once_with(type="CHAT", data=expected_message)
    assert result == 0

def test_send_data_with_retries(chat_instance, network_mock):
    # Asserting 9 of 10 retries used and then correctly send
    expected_message = "Hello, World!"
    network_mock.send_data.side_effect = [False] * 9 + [True]
    result = chat_instance.sendData(expected_message)
    assert network_mock.send_data.call_count == 10
    assert result == 0

def test_send_data_retry_exceeded(chat_instance, network_mock, caplog):
    # Asserting max retries used and then correctly failed 
    expected_message = "Hello, World!"
    network_mock.send_data.return_value = False
    result = chat_instance.sendData(expected_message)
    assert network_mock.send_data.call_count == 11
    assert "Fehler beim Senden von Chat-Nachrichten" in caplog.text
    assert f"Player: player1, Nachricht: {expected_message}" in caplog.text
    assert result == -1

def test_send_data_exception(chat_instance, network_mock, caplog):
    # Asserting exception is correctly thrown
    expected_message = "Hello, World!"
    network_mock.send_data.side_effect = Exception("Some error message")
    result = chat_instance.sendData(expected_message)
    network_mock.send_data.assert_called_once_with(type="CHAT", data=expected_message)
    assert "Allgemeiner Fehler beim Senden von Chat-Nachrichten von Player: player1" in caplog.text
    assert result == None