import obd


class obd2Reader():

    def __init__(self):

        self._connection = obd.OBD()  # auto-connects to USB or RF port
        self._connection = obd.OBD()  # auto-connects to USB or RF port
        self._cmd_speed = obd.commands.SPEED  # select an OBD command (sensor)
        self._cmd_FUEL_LEVEL = obd.commands.FUEL_LEVEL
        self._cmd_CONTROL_MODULE_VOLTAGE = obd.commands.CONTROL_MODULE_VOLTAGE
        self._cmd_AMBIANT_AIR_TEMP = obd.commands.AMBIANT_AIR_TEMP
        self._cmd_OIL_TEMP = obd.commands.OIL_TEMP
        self._cmd_RPM       = obd.commands.RPM
        #         self.RELATIVE_ACCEL_POS =  obd.commands.RELATIVE_ACCEL_POS


    @property
    def rpm(self):
        self._RPM = self.executeCommand(self.cmd_RPM)
        return self._RPM


    @property
    def speed(self):
        self._speed = self.executeCommand(self.cmd_speed)
        return self._speed

    @property
    def fuel_level(self):
        self._FUEL_LEVEL = self.executeCommand(self._cmd_FUEL_LEVEL)
        return self._FUEL_LEVEL

    @property
    def voltage(self):
        self._CONTROL_MODULE_VOLTAGE = self.executeCommand(self.cmd_CONTROL_MODULE_VOLTAGE)
        return self._CONTROL_MODULE_VOLTAGE

    @property
    def ambiant_air_temp(self):
        self._AMBIANT_AIR_TEMP = self.executeCommand(self.cmd_AMBIANT_AIR_TEMP)
        return self._AMBIANT_AIR_TEMP

    @property
    def oil_temp(self):
        self._OIL_TEMP= self.executeCommand(self.cmd_OIL_TEMP)
        return self._OIL_TEMP

    def close(self):
        self._connection.close()


