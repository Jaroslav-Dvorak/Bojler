import json
from collections import OrderedDict

SEEK_END = 2


def get_last_values(num_of_vals, filename, max_filesize=1024 * 100):
    try:
        with open(filename, "rb") as f:
            f.seek(0, SEEK_END)
            filesize = f.tell()
            if filesize < num_of_vals:
                f.seek(-filesize, SEEK_END)
                values_binary = f.read(filesize)
            else:
                f.seek(-num_of_vals, SEEK_END)
                values_binary = f.read(num_of_vals)
            values = [vb-127 for vb in values_binary]
    except OSError:
        return 0, []

    if filesize > max_filesize:
        with open(filename, "wb") as f:
            f.write(values_binary)
    return filesize, values


def save_value(value, filename):
    val_unsigned = value + 127
    val_binary = val_unsigned.to_bytes(1, "big")
    try:
        with open(filename, "ab") as f:
            f.write(val_binary)
    except OSError:
        with open(filename, "wb") as f:
            f.write(val_binary)


Settings = OrderedDict([
    ("WiFi-SSID", ""),
    ("WiFi-passw", ""),
    ("MQTT-brokr", ""),
    ("MQTT-user", ""),
    ("MQTT-passw", ""),
    ("MQTT-name", ""),
    ("widget", 0)
])


def settings_load():
    try:
        with open("settings.json", "r") as f:
            settings = f.read()
            settings = json.loads(settings)
    except Exception as e:
        print(e)
        return
    else:
        Settings.update(settings)


def settings_save():
    with open("settings.json", "w") as f:
        print(Settings)
        f.write(json.dumps(Settings))
