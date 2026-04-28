ENC_USERNAME = [0x30, 0x0D, 0x13, 0x2E, 0x09, 0x16, 0x24, 0x0D, 0x17, 0x00]
ENC_PASSWORD = [
    0x10,
    0x5B,
    0x13,
    0x78,
    0x09,
    0x49,
    0x24,
    0x5B,
    0x17,
    0x1B,
    0x51,
    0x5D,
    0x70,
    0x1F,
    0x0A,
    0x39,
    0x01,
    0x00,
]

KEY = "TheKey"


def de_xor(encrypted, key) -> str:

    key_idx = 0

    plaintext = ""

    for c in encrypted:

        plaintext += chr(ord(key[key_idx % len(key)]) ^ c)

        key_idx += 1

    return plaintext


print(
    f"username: {de_xor(ENC_USERNAME, KEY)[:-1]}, password: {de_xor(ENC_PASSWORD, KEY)[:-1]}"
)
