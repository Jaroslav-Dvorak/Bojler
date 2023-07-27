
SEEK_END = 2


def save_and_get_last_values(value, filename):
    num_of_rec = 249
    max_filesize = 1024*100

    val_unsigned = value + 127
    val_binary = val_unsigned.to_bytes(1, "big")

    with open(filename, "ab") as f:
        f.write(val_binary)

    with open(filename, "rb") as f:
        f.seek(0, SEEK_END)
        filesize = f.tell()
        if filesize < num_of_rec:
            f.seek(-filesize, SEEK_END)
            values_binary = f.read(filesize-1)
        else:
            f.seek(-num_of_rec, SEEK_END)
            values_binary = f.read(num_of_rec-1)
        values = [vb-127 for vb in values_binary]+[value]

    if filesize > max_filesize:
        with open(filename, "wb") as f:
            f.write(values_binary + val_binary)

    return values


# def save_and_get_last_values(value, filename):
#     num_of_rec = 10
#     max_filesize = 50
#
#     val_unsigned = value + 127
#     val_binary = val_unsigned.to_bytes(1, "big")
#     try:
#         with open(filename, "rb") as f:
#             f.seek(0, SEEK_END)
#             filesize = f.tell()
#             if filesize >= num_of_rec:
#                 f.seek(-num_of_rec, SEEK_END)
#                 values_binary = f.read(num_of_rec)
#             else:
#                 f.seek(-filesize, SEEK_END)
#                 values_binary = f.read(filesize - 1)
#             values = [vb - 127 for vb in values_binary] + [value]
#     except OSError:
#         with open(filename, "wb") as f:
#             f.write(val_binary)
#         return [value]
#
#     if filesize < max_filesize:
#         with open(filename, "ab") as f:
#             f.write(val_binary)
#     else:
#         with open(filename, "wb") as f:
#             f.write(values_binary + val_binary)
#
#     return values
