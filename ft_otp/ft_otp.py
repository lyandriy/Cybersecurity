import sys
import hashlib
import hmac
import re
import time
import struct
XOR_KEY = b"ft_otp_secret_xor_key_42"

def encrypted(file_key: str):
    try:
        content = open(file_key).read()
    except:
        print("./ft_otp: error: invalid file.")
        sys.exit(1)
    
    if len(content) < 64:
        print("./ft_otp: error: key must be 64 characters.")
        sys.exit(1)

    print (content)

    if not re.fullmatch(r"(0[xX])?[0-9a-fA-F]+", content):
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        sys.exit(1)

    key_in_bytes = bytes.fromhex(content)
    key = XOR_KEY

    encrypt = bytes([key_in_bytes[i] ^ key[i % len(key)] for i in range(len(key_in_bytes))])
    print(encrypt)

    try:
        file_otp_key = open("ft_otp.key", 'wb')
        file_otp_key.write(encrypt)
        file_otp_key.close()
        print("Key was successfully saved in ft_otp.key.")
    except:
        print("Error")

def temp_key(opt: str):
    try:
        with open(opt, "rb") as f:
            encrypt_key = f.read()
    except:
        print("./ft_otp: error: key file not found")
        sys.exit(1)

    count_time = int(time.time() // 30)
    msg = struct.pack('>Q', count_time)
    otp = hmac.new(encrypt_key, msg, hashlib.sha1).digest()
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error")
        sys.exit(1)
        sys.exit(1)

    if sys.argv[1] == "-g":
        encrypted(sys.argv[2])
    elif sys.argv[1] == "-k":
        temp_key(sys.argv[2])
    else:
        print("Error")
        sys.exit(1)