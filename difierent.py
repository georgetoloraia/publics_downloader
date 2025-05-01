from coincurve import PublicKey

# Your binary string (should be ≤256 bits for secp256k1)
zero_and_one = "1100010110000101111010011010101011000001100011100110011100100101011011101011010011011100000001010000101011010100110000010101100100101111010011010101100011100010000000101110011011111110100101001101011010001101000001001110110000110100100100010011001111110100"

# Ensure it's exactly 256 bits
zero_and_one = zero_and_one.zfill(256)[:256]

# Reconstruct private key
priv_key_int = int(zero_and_one, 2)
priv_key_bytes = priv_key_int.to_bytes(32, byteorder='big')

# Generate public key
pub = PublicKey.from_valid_secret(priv_key_bytes)
pub_uncompressed = pub.format(compressed=False)  # 65 bytes: 0x04 + x (32 bytes) + y (32 bytes)

# Extract x and y
pub_x = pub_uncompressed[1:33]  # bytes
pub_y = pub_uncompressed[33:]   # bytes

# Convert to binary
priv_key_bin = bin(priv_key_int)[2:].zfill(256)
pub_x_bin = bin(int.from_bytes(pub_x, 'big'))[2:].zfill(256)
pub_y_bin = bin(int.from_bytes(pub_y, 'big'))[2:].zfill(256)

# Print everything
print("🔐 Private Key (binary):")
print(priv_key_bin)
print("\n🔓 Public Key X (binary):")
print(pub_x_bin)
print("\n🔓 Public Key Y (binary):")
print(pub_y_bin)

# Compare public and private in bits
print("\n📊 Bit Differences:")
diff_x = sum(a != b for a, b in zip(priv_key_bin, pub_x_bin))
diff_y = sum(a != b for a, b in zip(priv_key_bin, pub_y_bin))
print(f"Diff between private key and pub.x: {diff_x} bits")
print(f"Diff between private key and pub.y: {diff_y} bits")
