

with open("allpubs1.txt", "r") as f:
    int_pubs = set(line for line in f)

with open("uncompress.txt", "a") as un:
    # uncompress = set(line for line in un)


    for i in int_pubs:
        if len(i) >= 66:
            mes = int(i[2:66], 16)
            un.write(f"{mes}\n")
