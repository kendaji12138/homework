import base64
from gmssl import sm2, sm3, sm4, func
import json
import random
import socket

alice_sk = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
alice_pk = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
bob_pk = 'F9B6F4D1F95F07DEDD9E182D9506480A7AE4E832BF08A09349420A646BC20A755ADF5B3F041FE664B2B6F32A76C007E961BB0AE06DC51D9DD21F647C39AC3A05'

share_key = "bupt-2016211628"

alice_enc = sm2.CryptSM2(
    public_key=bob_pk, private_key=0
)
alice_dec = sm2.CryptSM2(
    public_key=0, private_key=alice_sk
)
crypt_sm4 = sm4.CryptSM4()

a = random.randint(1, 9999)
a_enc = alice_enc.encrypt(str(a).encode())
# base64: binary<->bytes
send_data = {"a": base64.b64encode(a_enc).decode()}
send_data = json.dumps(send_data)
s = socket.socket()
s.connect("127.0.0.1", 1001)
s.send(send_data.encode())

recv_data = s.recv(1024)
recv_data = json.loads(recv_data.decode())
enc_b = base64.b64decode(recv_data['b'].encode())
b = alice_dec.decrypt(enc_b)
c = a*int(b.decode())
digest = recv_data['c_digest']
if sm3.sm3_hash(func.bytes_to_list(str(c).encode())) == digest:
    crypt_sm4.set_key(share_key, sm4.SM4_ENCRYPT)
    enc_c = crypt_sm4.crypt_ecb(str(c).encode())
    print("share key:", enc_c)
else:
    print("share key negotiation failed!")


