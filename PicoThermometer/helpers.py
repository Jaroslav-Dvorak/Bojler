

def num_to_byte(num, minimum, maximum):
    num = max(minimum, min(num, maximum))
    byte = int(((num - minimum) / (maximum - minimum)) * 256)
    byte = max(0, min(byte, 255))
    return byte


def byte_to_num(byte, minimum, maximum):
    byte = max(0, min(byte, 255))
    num = minimum + (byte / 255) * (maximum - minimum)
    return num


def voltage_to_soc(voltage):
    max_batt_volt = 4.20
    min_batt_volt = 2.80
    soc = int(((voltage - min_batt_volt) / (max_batt_volt - min_batt_volt)) * 100)
    if soc > 100:
        soc = 100
    elif soc < 0:
        soc = 0
    return soc
