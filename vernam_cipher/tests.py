from vernam_cipher import encrypt, decrypt

key = "vpELLEeIarPijBwIEryq"
salt = "VYCSEiWfwpDNfI"
pw = "lemon"
pw_s = pw + salt

print(pw_s)
hashpw = str(hash(pw_s))
print(hashpw)
print(encrypt(hashpw, key))
