import logging, time
from networking import Network

logging.basicConfig(level=logging.INFO)

TIMOUT_INTERVAL = 1 # Seconds

class Chat:
    def __init__(self, id: str) -> None:
        """
        A class to manage the chat within a game session for a local and remote player.
        
        Parameters:
            id (str): The unique identifier for the local player.

        """
        self.id = id

    def receiveData(self, id: str) -> str:
        """Receive chat-data throughout the game"""
        while True:

            try:
                message = Network.recv_data()

                # Anzeigen der Nachricht
                logging.info(f"[Receive-Data] Player: {id} received message {message}")
                return message
            
            except Exception:
                logging.error(f"[Receive-Data] Fehler beim Empfangen von Chat-Nachricht: Player: {id}")
                return "Fehler"

    def sendData(self, message: str) -> int:
        """Send chat-data if user wants to chat"""
        retry = 0
        
        try:
            success = Network.send_data(type="CHAT", data=message)

            while not success and retry < 10: # Re-send (try 10 times)

                success = Network.send_data(type="CHAT", data=message)
                retry += 1
                time.sleep(TIMOUT_INTERVAL)

                if not success and retry == 10:
                    logging.error(f"[Send-Data] Fehler beim Senden von Chat-Nachrichten: Player: {self.id}, Nachricht: {message}")
                    return -1
            
            logging.info(f"[Send-Data] Player: {self.id} send message {message}")

            return 0

        except Exception:
            logging.error(f"[Send-Data] Allgemeiner Fehler beim Senden von Chat-Nachrichten von Player: {self.id}")