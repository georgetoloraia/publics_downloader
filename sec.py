import multiprocessing
from random import randint
import time

class ECPoint:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

class Secp256k1:
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    G = ECPoint(
        x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    )
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    @staticmethod
    def point_add(p1, p2):
        if p1.infinity:
            return p2
        if p2.infinity:
            return p1
        if p1.x == p2.x and p1.y != p2.y:
            return ECPoint(None, None, infinity=True)
        if p1.x == p2.x and p1.y == p2.y:
            if p1.y == 0:
                return ECPoint(None, None, infinity=True)
            lam = ((3 * p1.x**2 + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
        else:
            lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p
        x3 = (lam**2 - p1.x - p2.x) % Secp256k1.p
        y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.p
        return ECPoint(x3, y3)

    @staticmethod
    def scalar_mult(k, point):
        result = ECPoint(None, None, infinity=True)
        addend = point
        while k:
            if k & 1:
                result = Secp256k1.point_add(result, addend)
            addend = Secp256k1.point_add(addend, addend)
            k >>= 1
        return result, addend

    @staticmethod
    def scalar_mult_original(k, point):
        result = ECPoint(None, None, infinity=True)
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

N = Secp256k1.n
ma = 2**67

with open("minuses.txt", "r") as all:
    pr = [int(pubs) for pubs in all]

with open("uncompress.txt", "r") as f:
    int_pubs = set(int(line) for line in f)

def process_range(i):
    # while i > ma:
    private_key = randint(1, N)
    private_key = private_key - i
    public_key, test = Secp256k1.generate_public_key(private_key)
    a = (public_key.x * public_key.y * test.x * test.y) % N
    b = Secp256k1.G.x
    c = Secp256k1.G.y
    d = (a + b) % N
    e = (a + b + d) % N
    f = (e + c) % N
    aa, _ = Secp256k1.generate_public_key_original(a)
    dd, _ = Secp256k1.generate_public_key_original(d)
    ee, _ = Secp256k1.generate_public_key_original(e)
    ff, _ = Secp256k1.generate_public_key_original(f)
    if aa.x in int_pubs or dd.x in int_pubs or ee.x in int_pubs or ff.x in int_pubs:
        print("W o W ..... !!!  Found..... !!!")
        print(f"{a}\n{d}\n{e}\n{f}")
        print()

if __name__ == "__main__":
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        pool.map(process_range, pr)
    end_time = time.time()
    print("Elapsed time:", end_time - start_time)
