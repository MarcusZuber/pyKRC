# src/pyKRC/connection.py
import socket


class Connection:
    def __init__(self, address: str = "localhost", port: int = 8080) -> None:
        """
        :param address: Name or IP of the kitten space agency remote control server
        :param port:  Port of the kitten space agency remote control server
        """
        self.address = address
        self.port = port

    def _send_command(self, command: str, recv_buf: int = 4096) -> str:
        """Sendet einen einfachen Textbefehl per TCP und liefert die Serverantwort zurück."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5.0)
                sock.connect((self.address, self.port))
                sock.sendall(command.encode("utf-8"))
                response = sock.recv(recv_buf).decode("utf-8").strip()
                return response
        except ConnectionRefusedError:
            raise ConnectionError(f"Could not connect to {self.address}:{self.port}")
        except Exception as e:
            raise RuntimeError(str(e))

    def _get(self, endpoint: str) -> str:
        """
        Asks the KSA server for data at the specified endpoint.
        :param endpoint: Pfad, z.B. /control/throttle
        :return: Wert als String (bei Erfolg) oder raises RuntimeError bei Fehlerantwort.
        """
        response = self._send_command(f"GET {endpoint}")
        if response.startswith("OK "):
            return response[3:]
        raise RuntimeError(response)

    def _set(self, endpoint: str, value: str) -> None:
        """
        Sends data to the KSA server at the specified endpoint.
        :param endpoint: Pfad, z.B. /control/throttle
        :param value: Wert, der gesetzt werden soll
        :raises RuntimeError: bei Fehlerantwort des Servers
        """
        response = self._send_command(f"SET {endpoint} {value}")
        if response == "OK":
            return
        raise RuntimeError(response)