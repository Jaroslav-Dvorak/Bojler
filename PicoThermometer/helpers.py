
ONBOARD_TEMP_CONV_TO_BYTE = (10, 250)
ONBOARD_TEMP_MINIMUM = 15
ONBOARD_TEMP_MAXIMUM = 35


def num_to_one_byte(value, delimiter, offset):
    one_byte_num = int((value * delimiter)-offset)
    if one_byte_num < -127:
        one_byte_num = -127
    elif one_byte_num > 128:
        one_byte_num = 128
    return one_byte_num


def one_byte_to_num(one_byte_num, delimiter, offset):
    val = (one_byte_num+offset) / delimiter
    val = round(val, 1)
    return val
