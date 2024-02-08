import sys
import socket
import logging
import time
from threading import Thread, Event

class Peer:
    def __init__(self, id: str, host: str, port: int, timeout: float) -> None:
        self.id = id
        self.host = host
        self.port = port
        self.peer_socket = None
        self.peer_client = None
        self.timeout = timeout
        self.shutdown_event = Event()
        self.potential_peers = []

    def discover(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("", self.port))
                
                while not self.shutdown_event.is_set():
                    sock.settimeout(self.timeout)
                    try:
                        data, addr = sock.recvfrom(1024)
                    except socket.timeout:
                        continue

                    if not data == bytes(self.id, 'utf-8'):
                        logging.info(f"[Peer-Verbindung] Broadcast erhalten von {addr} mit {data}")
                        self.add_peer((data.decode(), addr), time.time())
                    else:
                        logging.info(f"[Peer-Verbindung] Eigenen Broadcast empfangen: {addr}")
        except Exception as e:
            logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")

    def offer(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                while not self.shutdown_event.is_set(): 
                    msg = bytes(self.id, 'utf-8')
                    sock.sendto(msg, ("255.255.255.255", self.port))
                    self.shutdown_event.wait(1)
        except Exception as e:
            logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")

    def start_multiplayer(self) -> None:
        offer_thread = Thread(target=self.offer)
        offer_thread.start()

        discover_thread = Thread(target=self.discover)
        discover_thread.start()

        cleanup_thread = Thread(target=self.remove_stale_peers) 
        cleanup_thread.start()

        try:
            while True:
                if self.shutdown_event.is_set():
                    break
        except KeyboardInterrupt:
            self.shutdown_event.set()

        offer_thread.join()
        discover_thread.join()
        cleanup_thread.join()

    def stop_multiplayer(self) -> None:
        self.shutdown_event.set()

    def add_peer(self, peer_info: tuple, add_time=None) -> None:
        if add_time is None:
            add_time = time.time()
        peer_data = (peer_info[0], peer_info[1])
        if peer_data not in [peer[0] for peer in self.potential_peers]:
            self.potential_peers.append((peer_data, add_time))
            logging.info(f"[Peer-Verbindung] Neuer Peer hinzugefügt: {peer_data}")

    def remove_peer(self, peer_info) -> None:
        if peer_info in self.potential_peers:
            self.potential_peers.remove(peer_info)
            logging.info(f"[Peer-Verbindung] Peer entfernt: {peer_info}")

    def remove_stale_peers(self) -> None:
        while not self.shutdown_event.is_set():
            updated_potential_peers = []
            current_time = time.time()
            threshold = 20
            for peer, add_time in self.potential_peers:
                if current_time - add_time < threshold:
                    updated_potential_peers.append((peer, add_time))
            self.potential_peers = updated_potential_peers
            logging.info("[Peer-Verbindung] Alte Peers entfernt")
            time.sleep(10)

    def connect_peer_client(self, peer_host: str, peer_port: int) -> None:
        try:
            with socket.create_connection((peer_host, peer_port)) as self.peer_socket:
                logging.info(f"[Peer-Verbindung] Verbindung mit {peer_host}:{peer_port} erfolgreich")
                self.handle_connection()
        except socket.error as e:
            logging.error(f"[Peer-Verbindung] Verbindung mit {peer_host}:{peer_port} fehlgeschlagen. Error: {e}")

    def connect_peer_server(self) -> None:
        try:
            with socket.create_server((self.host, self.port)) as server:
                server.listen(1)
                logging.info(f"[Peer-Verbindung] Server aktiv auf {self.host}:{self.port}")
                server.settimeout(self.timeout)

                while not self.peer_client:
                    try:
                        self.peer_socket, self.peer_client = server.accept()
                        logging.info(f"[Peer-Verbindung] Verbindung mit {self.peer_client[1]} erfolgreich")

                    except socket.timeout:
                        logging.info("[Peer-Verbindung] Keine eingehende Verbindung, warte weiter...")
                        continue

                    except KeyboardInterrupt:
                        logging.info("[Peer-Verbindung] Server durch Benutzerunterbrechung beendet")
                        sys.exit(1)

                    except socket.error as e:
                        logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")
                        break

                keep = server.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
                if keep == 0:
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    logging.info("[Peer-Verbindung] Socket Keepalive aktiviert")
                else:
                    logging.info("[Peer-Verbindung] Socket Keepalive bereits aktiviert")

                self.handle_connection()

        except socket.error as e:
            logging.error(f"[Peer-Verbindung] Fehler bei der Verbindung: {e}")

    def handle_connection(self):
        #TODO
        pass


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    peer = Peer(id="example_id", host="localhost", port=5005, timeout=5.0)
    peer.start_multiplayer()

    # Zum Verbinden mit einem anderen Peer (Server-Modus)
    # peer.connect_peer_server()

    # Zum Verbinden mit einem anderen Peer (Client-Modus)
    # peer.connect_peer_client('peer_host_address', peer_port)