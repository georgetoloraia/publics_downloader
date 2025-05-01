from random import randint
import time

class ECPoint:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity  # Point at infinity (neutral element)

class Secp256k1:
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    G = ECPoint(
        x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    )
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    h = 1

    @staticmethod
    def point_add(p1, p2):
        # Handle the identity element (point at infinity)
        if p1.infinity:
            return p2
        if p2.infinity:
            return p1

        # Handle the case where p1 and p2 are reflections of each other over the x-axis
        if p1.x == p2.x and p1.y != p2.y:
            return ECPoint(None, None, infinity=True)

        # Handle the case where p1 and p2 are the same point (point doubling)
        if p1.x == p2.x and p1.y == p2.y:
            if p1.y == 0:
                return ECPoint(None, None, infinity=True)  # Tangent is vertical
            lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
        else:
            lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
        
        x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
        y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
        return ECPoint(x3, y3)

    @staticmethod
    def scalar_mult(k, point):
        # Simple and insecure scalar multiplication, not using double-and-add
        result = ECPoint(None, None, infinity=True)  # Start with the point at infinity
        addend = point
        test = 0

        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
                # print(result.x)
                # test += result.x
            addend = Secp256k1.point_add(addend, addend)
            # print(addend.x)
            # test += addend.x
            k >>= 1

        return result, addend
    
    @staticmethod
    def scalar_mult_original(k, point):
        # Simple and insecure scalar multiplication, not using double-and-add
        result = ECPoint(None, None, infinity=True)  # Start with the point at infinity
        addend = point
        test_list = []

        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
                test_list.append(result.x)
            addend = Secp256k1.point_add(addend, addend)
            test_list.append(addend.x)
            k >>= 1

        return result, test_list

    @staticmethod
    def generate_public_key(private_key):
        return Secp256k1.scalar_mult(private_key, Secp256k1.G)
    
    @staticmethod
    def generate_public_key_original(private_key):
        return Secp256k1.scalar_mult_original(private_key, Secp256k1.G)

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# Example usage:
'''
for private key we can enable all posible funqtions
'''
# with open("allpubs.txt", "r") as all:
#     pr = [int(pubs, 16) for pubs in all]

with open("minuses.txt", "r") as all:
    pr = [int(pubs) for pubs in all]

with open("uncompress.txt", "r") as f:
    int_pubs = set(int(line) for line in f)

start_time = time.time()
print(start_time)
ma = 2**67
for i in pr:
    print(i)
    while i > ma:
        private_key = randint(1, N)  # This should be a large, random number in a real application
        private_key = private_key - i
        # print(f"private key = {private_key}")
        public_key, test = Secp256k1.generate_public_key(private_key)
        # print(f"Public Key: ({hex(public_key.x)}, {hex(public_key.y)})")
    
    
        a = (public_key.x * public_key.y * test.x * test.y) % N
        b = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        c = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        d = (a + b) % N
        e = (a + b + d) % N
        f = (e + c) % N
        # print(f"a = {a}\nd = {d}\ne = {e}\nf = {f}")
    
        # print("started check ...................")
        aa, aa_list = Secp256k1.generate_public_key_original(a)
        dd, dd_list = Secp256k1.generate_public_key_original(d)
        ee, ee_list = Secp256k1.generate_public_key_original(e)
        ff, ff_list = Secp256k1.generate_public_key_original(f)


        # aa = Secp256k1.generate_public_key_original(a, Secp256k1.G)
        # dd = Secp256k1.generate_public_key_original(d, Secp256k1.G)
        # ee = Secp256k1.generate_public_key_original(e, Secp256k1.G)
        # ff = Secp256k1.generate_public_key_original(f, Secp256k1.G)
    
        # print(f"04{hex((public_key.x))[2:].zfill(64)}{hex(public_key.y)[2:].zfill(64)}")
        # print(f"04{hex(aa.x)[2:].zfill(64)}{hex(aa.y)[2:].zfill(64)}")
        # print(f"04{hex(dd.x)[2:].zfill(64)}{hex(dd.y)[2:].zfill(64)}")
        # print(f"04{hex(ee.x)[2:].zfill(64)}{hex(ee.y)[2:].zfill(64)}")
        # print(f"04{hex(ff.x)[2:].zfill(64)}{hex(ff.y)[2:].zfill(64)}")
        
    
        if aa.x in int_pubs or dd.x in int_pubs or ee.x in int_pubs or ff.x in int_pubs:
            print("W o W ..... !!!  Found..... !!!")
            print(f"{a}\n{d}\n{e}\n{f}")
            print()

        # for a_l in aa_list:
        #     if a_l in int_pubs:
        #         print(f"steps in {a}")

        # for d_l in dd_list:
        #     if d_l in int_pubs:
        #         print(f"steps in {d}")

        # for e_l in ee_list:
        #     if e_l in int_pubs:
        #         print(f"steps in {e}")

        # for f_l in ff_list:
        #     if f_l in int_pubs:
        #         print(f"steps in {f}")

        # i >>= 1

end_time = time.time()
print(end_time - start_time)