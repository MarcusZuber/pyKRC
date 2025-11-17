from .connection import Connection


class Telemetry(Connection):
    @property
    def altitude(self) -> float:
        """
        Gets the current altitude of the spacecraft.
        :return: Altitude in meters.
        """
        return 0

    @property
    def apoapsis(self) -> float:
        """
        Gets the current apoapsis of the spacecraft.
        :return: Apoapsis in meters.
        """
        data = self._get("/telemetry/apoapsis")
        return float(data)

    @property
    def periapsis(self) -> float:
        """
        Gets the current periapsis of the spacecraft.
        :return: Periapsis in meters.
        """
        data = self._get("/telemetry/periapsis")
        return float(data)
