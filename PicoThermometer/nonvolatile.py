
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
        return []

    if filesize > max_filesize:
        with open(filename, "wb") as f:
            f.write(values_binary)
    return values


def save_value(value, filename):
    val_unsigned = value + 127
    val_binary = val_unsigned.to_bytes(1, "big")
    with open(filename, "ab") as f:
        f.write(val_binary)
