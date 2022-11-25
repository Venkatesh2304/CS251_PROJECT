from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto.Cipher import AES
from Crypto import Random


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

base64pad = lambda s: s + b'=' * (4 - len(s) % 4)
base64unpad = lambda s: s.rstrip(b"=")
encrypt_key = 'LKHlhb899Y09olUi'


def encrypt(key, msg):
    iv = Random.new().read(BS)
    cipher = AES.new(key.encode(), AES.MODE_CFB, iv)
    encrypted_msg = cipher.encrypt( pad(str(msg)).encode() )
    return base64unpad(urlsafe_b64encode(iv + encrypted_msg))


# when incorrect encryption key is used, `decrypt` will return empty string
def decrypt(key, msg):
    decoded_msg = urlsafe_b64decode(base64pad(msg))
    iv = decoded_msg[:BS]
    encrypted_msg = decoded_msg[BS:] 
    cipher = AES.new(key.encode(), AES.MODE_CFB, iv)
    return unpad(cipher.decrypt(encrypted_msg))

hidden_msg = encrypt(encrypt_key, "Hello Wordsjkbfsdh<dsjfsdb,jld")
print( hidden_msg.decode() )
print(decrypt(encrypt_key, hidden_msg))  # Hello World