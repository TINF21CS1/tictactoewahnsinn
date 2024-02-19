import socket, logging, time, json, threading
from threading import Thread, Event, Lock
from typing import List, Optional, Tuple

logging.basicConfig(level=logging.INFO)

BUFFER_SIZE = 1024
ACKNOWLEDGMENT = "ACK"
DISCOVERY_OFFER = "DO"
PLAY_REQUEST = "PR"
PEER_CLEANUP_THRESHOLD = 20 
PEER_CLEANUP_INTERVAL = 30 # in seconds
BROADCAST_INTERVAL = 3 # in seconds
CONNECTION_RETRY = 5


class Network:
    def __init__(self, id: str, host: str, port: int, discover_timeout: float, connection_timeout: float) -> None:
        """
        A class to manage network connections for a local player, including discovery and connection to peer players within a networked game or application.
        
        Parameters:
            id (str): The unique identifier for the local player.
            host (str): The IP address or hostname for the local player.
            port (int): The port number for the local player.
            discover_timeout (float): Timeout duration for peer discovery.
            connection_timeout (float): Timeout duration for connection establishment.
        """
        self.id = id
        self.host = host
        self.port = port
        self.peer_connection = None
        self.peer_address: Optional[Tuple[str, int]] = None

        self.broadcast_socket: Optional[socket.socket] = None
        self.connection_socket: Optional[socket.socket] = None

        self.discover_timeout = discover_timeout
        self.connection_timeout = connection_timeout

        self.peer_lock = Lock()
        self.shutdown_event = Event()
        self.potential_peers: List[Tuple[str, Tuple[str, int]]] = []


    def init_broadcast_socket(self) -> socket.socket:
        """Initializes the UDP socket for broadcasting and listening for discovery messages."""
        if not self.broadcast_socket:
            try:
                self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                self.broadcast_socket.bind(('', self.port))
                self.broadcast_socket.settimeout(self.discover_timeout)
                logging.info(f"[Socket-Broadcast] Broadcast Socket erstellt.")
                return self.broadcast_socket

            except Exception as e:
                logging.error(f"[Socket-Broadcast] Fehler bei Socketerstellung: {e}")
        else:
            return self.broadcast_socket


    def init_connection_socket(self) -> socket.socket:
        """Initializes the TCP socket for accepting connections from peers."""
        if not self.connection_socket:
            try:
                self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.connection_socket.bind((self.host, (self.port + 1)))
                self.connection_socket.settimeout(self.connection_timeout)

                if not self.connection_socket.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE):
                    self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    logging.info("[Socket-Connection] Socket Keepalive aktiviert")
                            
            except Exception as e:
                logging.error(f"[Socket-Connection] Fehler bei Socketerstellung: {e}")
        else:
            return self.connection_socket
        
    
    def init_peer_connection(self, addr: Tuple[str, int]):
        """Attempts to establish a client connection to a peer."""
        if not self.peer_connection:
            try:
                with socket.create_connection(addr) as conn:
                    self.peer_connection = conn
                    logging.info(f"[Peer-Verbindung] Verbindung mit {addr[0]}:{addr[1]} erfolgreich")
                    return self.peer_connection
                
            except Exception as e:
                logging.error(f"[Socket-Peer] Fehler bei Verbindungserstellung: {e}")
        else:
            return self.peer_connection
        

    def get_potentialPeers(self) -> List[str]:
        """Retrieves a list of potential peer players discovered on the network."""
        return self.potential_peers.copy()
    

    def get_currentPeer(self) -> Optional[Tuple[str, int]]:
        """Retrieves the current peer's address as a tuple if a connection exists."""
        if self.peer_connection:
            try:
                return self.peer_connection.getpeername()
            except socket.error:
                return None
        return None


    def start_multiplayer(self) -> None:
        """Initiates the multiplayer networking process by starting the offer, discovery, and stale peer cleanup operations in separate threads."""
        threads = [
            Thread(target=self.offer),
            Thread(target=self.discover),
            Thread(target=self.remove_stale_peers)
        ]
        for thread in threads:
            thread.start()
            logging.info("[Multiplayer] Thread gestartet")
        try:
            while not self.shutdown_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("[Network] Stoppe Threads . . .")
            self.stop_multiplayer()
        for thread in threads:
            thread.join()

    
    def start_private_multiplayer(self, peer_host: str, peer_port: int) -> None:
        """Initiates a private multiplayer session by directly connecting to a specified peer."""
        for attempt in range(CONNECTION_RETRY):
            if self.connect_peer_client(peer_host, peer_port):
                    break
            logging.info(f"[Multiplayer-privat] Versuch {attempt + 1}: Verbindung fehlgeschlagen")
            time.sleep(2)
        if self.get_currentPeer == None:
            logging.error("[Multiplayer-privat] Es konnte keine Verbindung aufgebaut werden")
        self.handle_connection()


    def stop_multiplayer(self) -> None:
        """Signals all network operations to shut down gracefully."""
        self.shutdown_event.set()
        for _ in range(10):
            if not any(t.is_alive() for t in threading.enumerate() if t.name.startswith("Thread")):
                break
            time.sleep(0.5)
        self.shutdown_event.clear()
        if self.peer_connection:
            self.peer_connection.close()
        logging.info("[Shutdown] Multiplayer Threads wurden beendet")


    def offer(self) -> None:
        """Broadcasts this player's availability to the network. 'DO' = Discovery Offer """
        try:
            with self.init_broadcast_socket() as sock:
                while not self.shutdown_event.is_set(): 
                    msg = json.dumps({"id": self.id, "type": "DO", "addr": (self.host, self.port), "time": time.time()}).encode('utf-8')
                    sock.sendto(msg, ("255.255.255.255", self.port))
                    self.shutdown_event.wait(BROADCAST_INTERVAL)

        except Exception as e:
            logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")

    
    def discover(self) -> None:
        """Discovers peers on the network by listening for broadcast messages."""
        try:
            with self.init_broadcast_socket() as sock:
                while not self.shutdown_event.is_set():
                    try:
                        data, addr = sock.recvfrom(BUFFER_SIZE)
                    except socket.timeout:
                        continue
                    except Exception as e:
                        logging.error(f"[Peer-Discover] Fehler: {e}")
                    
                    if data:
                        json_data = json.loads(data.decode('utf-8'))
                        if json_data["id"] != self.id:
                            logging.info(f"[Peer-Verbindung] Broadcast erhalten von {addr} mit {json_data['type']}")

                        if json_data["type"] == "DO":
                            if json_data["id"] != self.id:
                                self.add_peer((json_data["id"], json_data["addr"]), time.time())
                            else:
                                logging.info(f"[Peer-Verbindung] Eigenen Broadcast empfangen: {addr}")
                        
                        elif json_data["type"] == PLAY_REQUEST:
                            self.connect_peer_server()
                            self.peer_address = json_data["addr"]
                            self.send_paket(sock, self.peer_address, ACKNOWLEDGMENT, PLAY_REQUEST)
                            
        except Exception as e:
            logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")

        
    def add_peer(self, peer_info: Tuple[str, Tuple[str, int]], add_time=None) -> None:
        """Adds a new peer to the list of potential peers."""
        with self.peer_lock:
            add_time = add_time or time.time()
            peer_data = (peer_info[0], peer_info[1])
            if peer_data not in [peer[0] for peer in self.potential_peers]:
                self.potential_peers.append((peer_data, add_time))
                logging.info(f"[Peer-Verbindung] Neuer Peer hinzugefügt: {peer_data}")       
    

    def remove_peer(self, peer_info: Tuple[str, Tuple[str, int]]) -> None:
        """Removes a peer from the list of potential peers."""
        if peer_info in self.potential_peers:
            self.potential_peers.remove(peer_info)
            logging.info(f"[Peer-Verbindung] Peer entfernt: {peer_info}")


    def remove_stale_peers(self) -> None:
        """Periodically checks and removes peers that are no longer responsive."""
        while not self.shutdown_event.is_set():
            with self.peer_lock:
                updated_potential_peers = []
                current_time = time.time()
                threshold = PEER_CLEANUP_THRESHOLD
                for peer, add_time in self.potential_peers:
                    if current_time - add_time < threshold:
                        updated_potential_peers.append((peer, add_time))
                self.potential_peers = updated_potential_peers
                logging.info("[Peer-Verbindung] Alte Peers entfernt")
                time.sleep(PEER_CLEANUP_INTERVAL)
            logging.info(f"[Potential Peers] {self.get_potentialPeers()}")


    def connect_peer_client(self, addr: Tuple[str, int]) -> bool:
        """Attempts to establish a client connection to a peer."""
        try:
            with self.init_peer_connection(addr) as conn:
                logging.info(f"[Peer-Verbindung] Verbindung mit {addr[0]}:{addr[1]} erfolgreich")
                self.handle_connection()
                return True
        except socket.error as e:
            logging.error(f"[Peer-Verbindung] Verbindung mit {addr[0]}:{addr[1]} fehlgeschlagen. Error: {e}")
            return False


    def connect_peer_server(self) -> None:
        """Starts a server to accept connections from peers."""  
        try:
            with self.init_connection_socket() as sock:
                with sock.create_server((self.host, self.port)) as server:
                    server.listen(1)
                    logging.info(f"[Peer-Verbindung] Server aktiv auf {self.host}:{self.port}")
                    while not self.shutdown_event.is_set():
                        try:
                            connection, client_address = server.accept()
                            self.peer_connection = connection
                            self.peer_address = client_address
                            logging.info(f"[Peer-Verbindung] Verbindung von {client_address} akzeptiert")
                        except socket.timeout:
                            logging.info("[Peer-Verbindung] Keine eingehende Verbindung")
                            continue
                        except socket.error as e:
                            logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")
                            break

                        if connection:
                            server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                            self.handle_connection()

        except socket.error as e:
            logging.error(f"[Peer-Verbindung] Fehler beim Starten des Servers: {e}")

    
    def join(self, addr: Tuple[str, int]):
        """Attempts to join a peer network by sending a play request to the specified address."""
        try:
            self.send_paket(addr, PLAY_REQUEST, "")
            response = self.recv_data()
            if response["type"] == ACKNOWLEDGMENT and response["data"] == PLAY_REQUEST:
                self.connect_peer_client(response["addr"][0], response["addr"][1])
        except Exception as e:
            logging.error(f"[join] Fehler bei der Verbindung: {e}")


    def send_paket(self, addr: Tuple[str, int], type: str, data: str):
        """Sends a packet with a specific type and data to the given address using a broadcast socket."""
        try:    
            with self.init_broadcast_socket() as sock:
                msg = json.dumps({"id": self.id, "type": type, "addr": (self.host, self.port), "time": time.time(), "data": data}).encode('utf-8')
                sock.sendto(msg, (addr[0], self.port))
        except socket.error as e:
            logging.error(f"[send-paket] Fehler bei der Übertragung: {e}")
        

    def send_data(self, addr: Tuple[str, int], type: str, data: str, send_time=None):
        """Sends data with a specific type to the given address over a peer connection."""
        send_time = send_time or time.time()
        try:
            with self.init_peer_connection(addr) as peer:
                peer.sendall(json.dumps({"id": self.id, "type": type, "addr": (self.host, self.port), "time": send_time, "data": data}).encode('utf-8'))
                logging.info("[send-data] Daten gesendet")

        except socket.error as e:
            logging.error(f"[send-data] Fehler bei der Übertragung: {e}")

    
    def recv_data(self) -> str:
        """Listens for incoming data from a peer connection."""
        while not self.shutdown_event.is_set():
            try:
                with self.init_peer_connection() as conn:
                    data = conn.recv(BUFFER_SIZE)
                    if data:
                        json_data = json.loads(data.decode('utf-8'))
                        logging.info(f"[recv-data] Daten erhalten: {json_data}")
                        return json_data
                    else:
                        logging.info("[recv-data] Verbindung geschlossen")
                        return None
            except socket.error as e:
                logging.error(f"[recv-data] Error: {e}")
                return None

    def handle_connection():
        """Placeholder function for handling game logic"""
        pass
