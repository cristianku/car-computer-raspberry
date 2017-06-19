import obd
from obd.utils import OBDStatus


class obd2Reader():

    def __init__(self):

        self._connection = obd.OBD()  # auto-connects to USB or RF port
        # print " ********* "
        # print " ********* "
        # print " ********* "
        # print " ********* "
        # print " ********* "
        # print " connection  "
        # print self._connection.status()
        # print " ********* "
        # print " ********* "
        # print " ********* "

        self._cmd_speed                     = obd.commands.SPEED  # select an OBD command (sensor)
        self._cmd_FUEL_LEVEL                = obd.commands.FUEL_LEVEL
        self._cmd_CONTROL_MODULE_VOLTAGE    = obd.commands.CONTROL_MODULE_VOLTAGE
        self._cmd_AMBIANT_AIR_TEMP          = obd.commands.AMBIANT_AIR_TEMP
        self._cmd_OIL_TEMP                  = obd.commands.OIL_TEMP
        self._cmd_RPM                       = obd.commands.RPM
        self._cmd_BAROMETRIC_PRESSURE       = obd.commands.BAROMETRIC_PRESSURE
        #         self.RELATIVE_ACCEL_POS =  obd.commands.RELATIVE_ACCEL_POS
        self._cmd_COOLANT_TEMP              = obd.commands.COOLANT_TEMP

        self._cmd_THROTTLE_POS_B            = obd.commands.THROTTLE_POS_B

        self._cmd_THROTTLE_POS_C            = obd.commands.THROTTLE_POS_C
        self._cmd_ACCELERATOR_POS_D         = obd.commands.ACCELERATOR_POS_D
        self._cmd_ACCELERATOR_POS_E         = obd.commands.ACCELERATOR_POS_E
        self._cmd_ACCELERATOR_POS_F         = obd.commands.ACCELERATOR_POS_F
        self._cmd_THROTTLE_ACTUATOR         = obd.commands.THROTTLE_ACTUATOR

    @property
    def throttle_act(self):
        self._throttle_act = self.executeCommand(self._cmd_THROTTLE_ACTUATOR)
        return self._throttle_act

    @property
    def throttle_b(self):
        self._throttle_b = self.executeCommand(self._cmd_THROTTLE_POS_B)
        return self._throttle_b


    @property
    def throttle_c(self):
        self._throttle_c = self.executeCommand(self._cmd_THROTTLE_POS_C)
        return self._throttle_c

    @property
    def accelerator_d(self):
        self._accelerator_d = self.executeCommand(self._cmd_ACCELERATOR_POS_D)
        return self._accelerator_d


    @property
    def accelerator_e(self):
        self._accelerator_e = self.executeCommand(self._cmd_ACCELERATOR_POS_E)
        return self._accelerator_e

    @property
    def accelerator_f(self):
        self._accelerator_f = self.executeCommand(self._cmd_ACCELERATOR_POS_F)
        return self._accelerator_f

    @property
    def barometric_pressure(self):
        self._barometric_pressure = self.executeCommand(self._cmd_BAROMETRIC_PRESSURE)
        return self._barometric_pressure

    @property
    def rpm(self):
        self._RPM = self.executeCommand(self._cmd_RPM)
        return self._RPM


    @property
    def speed(self):
        self._speed = self.executeCommand(self._cmd_speed)
        return self._speed

    @property
    def fuel_level(self):
        self._FUEL_LEVEL = self.executeCommand(self._cmd_FUEL_LEVEL)
        return self._FUEL_LEVEL

    @property
    def voltage(self):
        self._CONTROL_MODULE_VOLTAGE = self.executeCommand(self._cmd_CONTROL_MODULE_VOLTAGE)
        return self._CONTROL_MODULE_VOLTAGE

    @property
    def ambiant_air_temp(self):
        self._AMBIANT_AIR_TEMP = self.executeCommand(self._cmd_AMBIANT_AIR_TEMP)
        return self._AMBIANT_AIR_TEMP

    @property
    def oil_temp(self):
        self._OIL_TEMP= self.executeCommand(self._cmd_OIL_TEMP)
        return self._OIL_TEMP

    def executeCommand(self,cmd):
        if self._connection.status() == OBDStatus.NOT_CONNECTED:
            return ""
        else:
            response = self._connection.query(cmd)
            return response.value

    def close(self):
        self._connection.close()


