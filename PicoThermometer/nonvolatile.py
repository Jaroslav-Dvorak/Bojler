import json


SEEK_END = 2
Settings = {"full_refresh_cadence": 10}


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
    with open(filename, "ab") as f:
        f.write(val_binary)


def settings_load():
    # default = {"widget": 0}
    # try:
    #     with open("settings.json", "r") as f:
    #         settings = f.read()
    # except OSError:
    #     settings = default
    # else:
    #     settings = json.loads(settings)
    with open("settings.json", "r") as f:
        settings = f.read()
        settings = json.loads(settings)
    return settings


def settings_save(settings):
    settings = json.dumps(settings)
    print(settings)
    with open("settings.json", "w") as f:
        f.write(settings)
