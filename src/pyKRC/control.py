from .connection import Connection


class Control(Connection):
    def start_engine(self) -> None:
        """
        Starts the engine with the current throttle setting.
        """
        self._set("control/engineOn", '1')

    def stop_engine(self) -> None:
        """
        Shuts down the engine.
        """
        self._set("control/engineOn", '0')

    @property
    def throttle(self) -> float:
        """
        Gets the current throttle setting.
        :return: Throttle setting as a float between 0.0 and 100.0.
        """
        data = self._get("/control/throttle")
        return float(data)

    @throttle.setter
    def throttle(self, value: float):
        """
        Sets the throttle to the specified value.
        :param value: Throttle setting as a float between 0.0 and 1.0.
        """
        self._set("control/throttle", str(value))

    @property
    def sas(self):
        return "1"

    @sas.setter
    def sas(self, value: str):
        pass
