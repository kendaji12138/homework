import base64
from gmssl import sm2, sm3, sm4, func
import json
import random
import socket

bob_sk = '3C2AD19567B69AA3D64D051AD6CD94A8E2BD604933B21E78E63E18461A93FD92'
bob_pk = 'F9B6F4D1F95F07DEDD9E182D9506480A7AE4E832BF08A09349420A646BC20A755ADF5B3F041FE664B2B6F32A76C007E961BB0AE06DC51D9DD21F647C39AC3A05'
alice_pk = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

share_key = "bupt-2016211628"

bob_enc = sm2.CryptSM2(
    public_key=alice_pk, private_key=0
)
bob_dec = sm2.CryptSM2(
    public_key=0, private_key=bob_sk
)
crypt_sm4 = sm4.CryptSM4()

s = socket.socket()
s.bind("127.0.0.1", 1001)
s.listen()
conn, addr = s.accept()

recv_data = conn.recv(1024)
recv_data = json.loads(recv_data.decode())
enc_a = base64.b64decode(recv_data['a'].encode())
a = bob_dec.decrypt(enc_a).decode()

b = random.randint(1, 9999)
c = int(a)*b
crypt_sm4.set_key(share_key, sm4.SM4_ENCRYPT)
enc_c = crypt_sm4.crypt_ecb(str(c).encode())

enc_b = bob_enc.encrypt(str(b).encode())
send_data = {"b": base64.b64encode(enc_b), "c_digest": sm3.sm3_hash(func.bytes_to_list(str(c).encode()))}
send_data = json.dumps(send_data)
conn.send(send_data.encode())

print("share key:", enc_c)


