import sys
import socket
import logging

class Peer:
    def __init__(self, id: str, host: str, port: int, timeout: float) -> None:
        self.id = id
        self.host = host
        self.port = port
        self.socket = None
        self.client = None
        self.timeout = timeout

    def handle_connection(self):
        #TODO
        pass

    def connect(self, peer_host: str, peer_port: int) -> None:
        try:
            with socket.create_connection((peer_host, peer_port)) as self.socket:
                logging.info(f"[Peer-Verbindung] Verbindung mit {peer_host}:{peer_port} erfolgreich")
                self.handle_connection()
        except socket.error as e:
            logging.error(f"[Peer-Verbindung] Verbindung mit {peer_host}:{peer_port} fehlgeschlagen. Error: {e}")

    def start_server(self) -> None:
        try:
            with socket.create_server((self.host, self.port)) as server:
                server.listen(1)
                logging.info(f"[Peer-Verbindung] Server aktiv auf {self.host}:{self.port}")
                server.settimeout(self.timeout)

                while not self.client:
                    try:
                        self.client = server.accept()
                        logging.info(f"[Peer-Verbindung] Verbindung mit {self.client[1]} erfolgreich")

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


    def close_connection(self) -> None:
        if self.socket:
            self.socket.close()
            logging.info("[Peer-Verbindung] Verbindung geschlossen.")




logging.basicConfig(level=logging.INFO)

peer = Peer('example_id', 'localhost', 5000, 5.0)

# Zum Verbinden mit einem anderen Peer (Server-Modus)
peer.start_server()

# Zum Verbinden mit einem anderen Peer (Client-Modus)
# peer.connect('peer_host_address', peer_port)

