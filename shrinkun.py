
with open("allpubs1.txt", "r") as f:
    int_pubs = set(line for line in f)

with open("rmd.txt", "a") as un:
    # uncompress = set(line for line in un)


    for i in int_pubs:
        # print(i)
        if 48 == len(i):
            print(f"{i[4:40]}")
            mes = int(i[4:40], 16)
            un.write(f"{mes}\n")
        if len(i) == 40:
            mes = int(i, 16)
            un.write(f"{mes}\n")

print(len("a914b10782f66b4c524d7b7e8fddf281c6f23b052e6f88ac"))
print(len("9b085b7913815fe750b197fa6d4406ab6b22f978"))

"""
a914 b10782f66b4c524d7b7e8fddf281c6f23b052e6f 88ac
"""