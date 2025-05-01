from coincurve import PublicKey

# Binary sequence (example)
zero_and_one = "110001001110000010011101111000011000011111101001010011101011101101110110000000100000100110010110100011101010001111000111111100111110111001100000011111010001000010010101110111110111111100001110111110111101111111001011001010100001110110010011011011000100011010101100"  # replace with your real binary string

# Start with base point G (the generator point)
G = PublicKey.from_valid_secret(b'\x01')  # This gives us G

acc = None  # This will accumulate the result

for bit in zero_and_one:
    if acc is None:
        acc = G
    else:
        # Always double the current point (by adding it to itself)
        acc = PublicKey.combine_keys([acc, acc])

    if bit == '1':
        # Add base point G
        acc = PublicKey.combine_keys([acc, G])

# Print final X-coordinate of the resulting public key
uncompressed = acc.format(compressed=False).hex()
x_coord = uncompressed[2:66]  # Skip the 0x04 prefix
print(x_coord)
print("Final X-coordinate:", int(x_coord, 16))
