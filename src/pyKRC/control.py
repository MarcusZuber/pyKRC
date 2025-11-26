from .connection import Connection


class Control(Connection):
    def start_engine(self) -> None:
        """
        Starts the engine with the current throttle setting.
        """
        self._set("/control/engineOn", {"engineOn": True})

    def stop_engine(self) -> None:
        """
        Shuts down the engine.
        """
        self._set("/control/engineOn", {"engineOn": False})

    @property
    def engine_on(self) -> bool:
        """
        Gets the current engine state.
        :return: True if engine is on, False otherwise.
        """
        data = self._get("/control/engineOn")
        return bool(data["engineOn"])

    @engine_on.setter
    def engine_on(self, value: bool):
        """
        Sets the engine state.
        :param value: True to turn engine on, False to turn off.
        """
        self._set("/control/engineOn", {"engineOn": value})

    @property
    def throttle(self) -> float:
        """
        Gets the current throttle setting.
        :return: Throttle setting as a float between 0.0 and 1.0.
        """
        data = self._get("/control/throttle")
        return float(data["throttle"])

    @throttle.setter
    def throttle(self, value: float):
        """
        Sets the throttle to the specified value.
        :param value: Throttle setting as a float between 0.0 and 1.0.
        """
        self._set("/control/throttle", {"throttle": value})

    @property
    def reference_frame(self) -> str:
        """
        Gets the current reference frame.
        :return: Reference frame name (e.g., "LVLH").
        """
        data = self._get("/control/referenceFrame")
        return str(data["frame"])

    @reference_frame.setter
    def reference_frame(self, value: str | int):
        """
        Sets the reference frame.
        :param value: Reference frame name (string) or ID (int).
        """
        self._set("/control/referenceFrame", {"frame": value})

    def get_reference_frames(self) -> list[dict]:
        """
        Gets all available reference frames.
        :return: List of reference frames with name and value.
        """
        data = self._get("/control/referenceFrames")
        return data["frames"]

    @property
    def attitude_mode(self) -> str | None:
        """
        Gets the current flight computer attitude mode.
        :return: Attitude mode name or None if not set.
        """
        data = self._get("/control/flightComputer/attitudeMode")
        return data["attitudeMode"]

    @attitude_mode.setter
    def attitude_mode(self, value: str | int):
        """
        Sets the flight computer attitude mode.
        :param value: Attitude mode name (string) or ID (int).
        """
        self._set("/control/flightComputer/attitudeMode", {"mode": value})

    def get_attitude_modes(self) -> list[dict]:
        """
        Gets all available flight computer attitude modes.
        :return: List of attitude modes with name and value.
        """
        data = self._get("/control/flightComputer/attitudeModes")
        return data["modes"]

    def set_stabilization(self, enabled: bool) -> None:
        """
        Enables or disables spacecraft stabilization.
        :param enabled: True to enable stabilization, False to disable.
        """
        self._set("/control/flightComputer/stabilization", {"stabilization": enabled})

    def get_thrusters(self) -> dict:
        """
        Get current thruster command flags.
        :return: Dict mapping thruster enum names to booleans.
        """
        data = self._get("/control/thrusters")
        # The API may return { "thrusters": { ... } } or the mapping directly.
        if isinstance(data, dict) and "thrusters" in data and isinstance(data["thrusters"], dict):
            return data["thrusters"]
        if isinstance(data, dict):
            # assume data itself is the mapping
            return data
        return {}

    def set_thrusters(self, thrusters: dict) -> dict:
        """
        Batch-set thruster command flags (partial update supported by server).
        :param thrusters: Mapping of thruster names to boolean/number/string values.
        :return: Updated thruster mapping as returned by the server.
        """
        payload = thrusters
        # If user passed a dict that isn't wrapped, wrap under 'thrusters' to match one of the accepted shapes
        if "thrusters" not in payload:
            payload = {"thrusters": thrusters}
        # Use POST for batch thruster updates per OpenAPI
        response = self._post("/control/thrusters", payload)
        if isinstance(response, dict) and "thrusters" in response:
            return response["thrusters"]
        if isinstance(response, dict):
            return response
        return {}

    @property
    def sas(self):
        """
        Deprecated: Use stabilization methods instead.
        """
        return "1"

    @sas.setter
    def sas(self, value: str):
        """
        Deprecated: Use stabilization methods instead.
        """
        pass
