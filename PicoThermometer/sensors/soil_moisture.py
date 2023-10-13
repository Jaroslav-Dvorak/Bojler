from collections import OrderedDict


class SoilMoisture:
    def __init__(self, adc):
        self.adc = adc
        self.minimum = 18000
        self.maximum = 40000

        self.displ_min = 0
        self.displ_max = 100

    def _measure(self):
        num_of_measurements = 1000
        n = 0
        measured = 0
        while n < num_of_measurements:
            measured += self.adc.read_u16()
            n += 1
        value = (measured / num_of_measurements)
        return 65535-int(value)

    def cont_measure(self):
        while True:
            print(self._to_percentage(self._measure()))

    def _to_percentage(self, val):
        val = max(self.minimum, min(val, self.maximum))
        val -= self.minimum
        diff = self.maximum - self.minimum
        val /= diff
        return int(val*100)

    def get_serial(self):
        return "value:" + str(self._measure())

    def get_values(self):
        values = OrderedDict()
        values["moisture"] = self._to_percentage(self._measure())
        return values

    def setup_sensor(self):
        from nonvolatile import Settings
        self.minimum = int(Settings["Minimum"])
        self.maximum = int(Settings["Maximum"])

    @property
    def params(self):
        sensor_settings = OrderedDict()
        sensor_settings["Minimum"] = self.minimum
        sensor_settings["Maximum"] = self.maximum
        return sensor_settings
