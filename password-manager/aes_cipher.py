from Crypto.Cipher import AES
import json
import hashlib
import os


def pad_string(s):
    s_padded = s + " " * (16 - len(s) % 16)
    return s_padded


def encrypt_passwords(passwords, master_password, filename):
    key = hashlib.sha256(master_password.encode()).digest()
    plain_text = pad_string(json.dumps(passwords))
    iv = os.urandom(16)
    cipher = AES.new(key, iv=iv, mode=AES.MODE_CBC)

    cipher_text = cipher.encrypt(plain_text.encode())
    with open(filename, "bw") as f:
        f.write(cipher_text + iv)


def decrypt_passwords(master_password, filename):
    key = hashlib.sha256(master_password.encode()).digest()
    cipher_text = b''
    with open(filename, "br") as f:
        for line in f.readlines():
            cipher_text += bytes(line)
    iv = cipher_text[-16:]
    cipher_text = cipher_text[:-16]
    cipher = AES.new(key, iv=iv, mode=AES.MODE_CBC)

    plain_text = cipher.decrypt(cipher_text).decode()
    return json.loads(plain_text)


if __name__ == "__main__":
    print()

    pass
