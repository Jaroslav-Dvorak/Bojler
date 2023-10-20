from collections import OrderedDict
import json

class SoilMoisture:
    def __init__(self, adc, filename):
        self.adc = adc

        self.displ_min = 0
        self.displ_max = 100

        self.filename = filename
        self.settings = self.settings_load()
        self.minimum = int(self.settings["Minimum"])
        self.maximum = int(self.settings["Maximum"])
        self.minimum = 18000
        self.maximum = 40000

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
        minimum, maximum = int(self.minimum), int(self.maximum)
        val = max(minimum, min(val, maximum))
        val -= minimum
        diff = maximum - minimum
        val /= diff
        return int(val*100)

    @property
    def info(self):
        return "value:" + str(self._measure())

    def get_values(self):
        values = OrderedDict()
        values["moisture"] = self._to_percentage(self._measure())
        return values

    def settings_load(self):
        settings = OrderedDict()
        try:
            with open(self.filename, "r") as f:
                settings = f.read()
                settings = json.loads(settings)
        except Exception as e:
            print(e)
            settings["Minimum"] = "18000"
            settings["Maximum"] = "40000"
        finally:
            return settings

    def settings_save(self):
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.settings))
