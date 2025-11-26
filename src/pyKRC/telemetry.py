from .connection import Connection


class Telemetry(Connection):
    @property
    def altitude(self) -> float:
        """
        Gets the current altitude of the spacecraft.
        :return: Altitude in meters.
        """
        # Note: altitude endpoint is not defined in the OpenAPI spec yet
        # Placeholder implementation
        return 0

    @property
    def apoapsis(self) -> float:
        """
        Gets the current apoapsis of the spacecraft.
        :return: Apoapsis in meters.
        """
        data = self._get("/telemetry/apoapsis")
        return float(data["apoapsis"])

    @property
    def periapsis(self) -> float:
        """
        Gets the current periapsis of the spacecraft.
        :return: Periapsis in meters.
        """
        data = self._get("/telemetry/periapsis")
        return float(data["periapsis"])

    @property
    def apoapsis_elevation(self) -> float:
        """
        Gets the apoapsis elevation above surface (apoapsis - mean radius).
        :return: Apoapsis elevation in meters.
        """
        data = self._get("/telemetry/apoapsis_elevation")
        return float(data["apoapsisElevation"])

    @property
    def periapsis_elevation(self) -> float:
        """
        Gets the periapsis elevation above surface (periapsis - mean radius).
        :return: Periapsis elevation in meters.
        """
        data = self._get("/telemetry/periapsis_elevation")
        return float(data["periapsisElevation"])

    @property
    def orbital_speed(self) -> float:
        """
        Gets the current orbital speed of the vessel.
        :return: Orbital speed in m/s.
        """
        data = self._get("/telemetry/orbitalSpeed")
        return float(data["orbitalSpeed"])

    @property
    def propellant_mass(self) -> float:
        """
        Gets the current propellant mass of the vessel.
        :return: Propellant mass in kg.
        """
        data = self._get("/telemetry/propellantMass")
        return float(data["propellantMass"])

    @property
    def total_mass(self) -> float:
        """
        Gets the total mass of the vessel.
        :return: Total mass in kg.
        """
        data = self._get("/telemetry/totalMass")
        return float(data["totalMass"])

    @property
    def mean_radius(self) -> float:
        """
        Gets the mean radius of the body being orbited.
        :return: Mean radius in meters.
        """
        data = self._get("/telemetry/orbitingBody/meanRadius")
        return float(data["meanRadius"])
