from .connection import Connection


class Telemetry(Connection):
    @property
    def altitude(self) -> float:
        """
        Gets the current altitude of the spacecraft.
        :return: Altitude in meters.
        """
        data = self._get("telemetry/altitude")
        return data.get('value', 0.0)

    @property
    def apoapsis(self) -> float:
        """
        Gets the current apoapsis of the spacecraft.
        :return: Apoapsis in meters.
        """
        data = self._get("telemetry/apoapsis")
        return data.get('value', 0.0)

    @property
    def periapsis(self) -> float:
        """
        Gets the current periapsis of the spacecraft.
        :return: Periapsis in meters.
        """
        data = self._get("telemetry/periapsis")
        return data.get('value', 0.0)
