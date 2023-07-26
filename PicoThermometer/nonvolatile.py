import random
filename = "temperatures.dat"
for _ in range(1):
    with open(filename, "ab") as f:
        tmp = random.randint(-127, 128)
        tmp_unsigned = tmp + 127
        msg = tmp_unsigned.to_bytes(1, "big")
        print(tmp)
        f.write(msg)
print("*"*10)
num_of_rec = 5
max_filesize = 20

with open(filename, "rb") as f:
    f.seek(0, 2)    # 2=os.SEEK_END
    filesize = f.tell()
    if filesize < num_of_rec:
        f.seek(-filesize, 2)    # 2=os.SEEK_END
        cont = f.read(filesize-1)
    else:
        f.seek(-num_of_rec, 2)    # 2=os.SEEK_END
        cont = f.read(num_of_rec-1)
    tmps = [b-127 for b in cont]+[tmp]
    print(tmps)

if filesize > max_filesize:
    with open(filename, "wb") as f:
        f.write(cont+msg)
