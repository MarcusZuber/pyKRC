import requests


class Connection:
    def __init__(self, address: str = "localhost", port: int = 8080, use_https: bool = False) -> None:
        """
        :param address: Name or IP of the kitten space agency remote control server
        :param port:  Port of the kitten space agency remote control server
        :param use_https: Use HTTPS for the connection (not yet implemented in the server.)
        """
        self.address = address
        self.port = port
        self.use_https = use_https

    def _get(self, endpoint: str) -> dict:
        """
        Asks the KSA server for data at the specified endpoint.
        :param endpoint:
        :return: Dictionary with the requested data.
        """
        if self.use_https:
            url = f"https://{self.address}:{self.port}/{endpoint}"
        else:
            url = f"http://{self.address}:{self.port}/{endpoint}"

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _set(self, endpoint: str, data: dict) -> None:
        """
        Sends data to the KSA server at the specified endpoint.
        :param endpoint:
        :param data: Dictionary with the data to send.
        """
        if self.use_https:
            url = f"https://{self.address}:{self.port}/{endpoint}"
        else:
            url = f"http://{self.address}:{self.port}/{endpoint}"

        response = requests.post(url, json=data)
        response.raise_for_status()
