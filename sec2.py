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
        if p1.x == p2.x:
            if p1.y == 0:
                return ECPoint(None, None, infinity=True)
            lam = ((3 * p1.x * p1.x + Secp256k1.a) * pow(2 * p1.y, -1, Secp256k1.p)) % Secp256k1.p
        else:
            lam = ((p2.y - p1.y) * pow(p2.x - p1.x, -1, Secp256k1.p)) % Secp256k1.p

        x3 = (lam * lam - p1.x - p2.x) % Secp256k1.p
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
        return result

    @staticmethod
    def generate_public_key(private_key):
        return Secp256k1.scalar_mult(private_key, Secp256k1.G)

# Load input
with open("minuses.txt", "r") as all_file:
    pr = [int(line.strip()) for line in all_file if line.strip()]

with open("uncompress.txt", "r") as f:
    int_pubs = set(int(line.strip()) for line in f if line.strip())

N = Secp256k1.n
total = len(pr)

# Shared counter and lock
counter = multiprocessing.Value("i", 0)
lock = multiprocessing.Lock()
logfile_lock = multiprocessing.Lock()

def process_range(i):
    private_key = (randint(1, N - 1) - i) % N
    for offset in range(4):  # try key, key+1, key+2, key+3
        k = (private_key + offset) % N
        public_point = Secp256k1.generate_public_key(k)
        if public_point.infinity:
            continue
        if public_point.x in int_pubs:
            message = (
                "\nW o W ..... !!!  Found..... !!!\n"
                f"Private key candidate: {k}\n"
                f"Matching pubkey x: {public_point.x}\n"
            )
            with lock:
                print(message)
            with logfile_lock:
                with open("found_keys.txt", "a") as log:
                    log.write(f"{k},{public_point.x}\n")

    with counter.get_lock():
        counter.value += 1
        progress = f"Processed {counter.value}/{total}"
        print(progress.ljust(50), end="\r", flush=True)

if __name__ == "__main__":
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        pool.map(process_range, pr)
    end_time = time.time()
    print("\nElapsed time:", end_time - start_time)
