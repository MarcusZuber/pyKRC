# src/pyKRC/connection.py
import requests


class Connection:
    def __init__(self, address: str = "localhost", port: int = 8080) -> None:
        """
        :param address: Name or IP of the kitten space agency remote control server
        :param port:  Port of the kitten space agency remote control server
        """
        self.address = address
        self.port = port
        self.base_url = f"http://{address}:{port}"

    def _get(self, endpoint: str) -> dict:
        """
        Asks the KSA server for data at the specified endpoint.
        :param endpoint: Pfad, z.B. /control/throttle
        :return: JSON response as dict
        :raises requests.exceptions.ConnectionError: wenn keine Verbindung hergestellt werden kann
        :raises RuntimeError: bei Fehlerantwort des Servers
        """
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=5.0)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError(f"Could not connect to {self.address}:{self.port}")
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get("error", str(e)) if e.response else str(e)
            raise RuntimeError(error_msg)

    def _set(self, endpoint: str, value: str | dict) -> dict:
        """
        Sends data to the KSA server at the specified endpoint using PUT.
        :param endpoint: Pfad, z.B. /control/throttle
        :param value: Wert, der gesetzt werden soll (als String für text/plain oder dict für JSON)
        :return: JSON response as dict
        :raises requests.exceptions.ConnectionError: wenn keine Verbindung hergestellt werden kann
        :raises RuntimeError: bei Fehlerantwort des Servers
        """
        try:
            if isinstance(value, dict):
                response = requests.put(f"{self.base_url}{endpoint}", json=value, timeout=5.0)
            else:
                response = requests.put(
                    f"{self.base_url}{endpoint}",
                    data=str(value),
                    headers={"Content-Type": "text/plain"},
                    timeout=5.0
                )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError(f"Could not connect to {self.address}:{self.port}")
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get("error", str(e)) if e.response else str(e)
            raise RuntimeError(error_msg)

    def _post(self, endpoint: str, value: str | dict) -> dict:
        """
        Sends data to the KSA server at the specified endpoint using POST.
        Used for endpoints that expect POST (e.g. /control/thrusters).
        :param endpoint: Pfad, z.B. /control/thrusters
        :param value: Wert (dict -> JSON, else text/plain)
        :return: JSON response as dict
        """
        try:
            if isinstance(value, dict):
                response = requests.post(f"{self.base_url}{endpoint}", json=value, timeout=5.0)
            else:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    data=str(value),
                    headers={"Content-Type": "text/plain"},
                    timeout=5.0
                )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError(f"Could not connect to {self.address}:{self.port}")
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get("error", str(e)) if e.response else str(e)
            raise RuntimeError(error_msg)
