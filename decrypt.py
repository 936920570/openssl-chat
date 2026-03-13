from Crypto.Cipher import AES
import sys
crypt_file_name = sys.argv[1]
crypt_file = open(crypt_file_name,"rb")
if crypt_file is None:
    print("No such file!")
passwd = input("Password:").encode('utf-8')
while len(passwd) <= 16:
    passwd = passwd + b'\x00'
passwd = passwd[0:16]
aes = AES.new(passwd,AES.MODE_ECB)
en_text = crypt_file.read()
den_text = aes.decrypt(en_text)
print("Chatting records:\n",den_text.decode())