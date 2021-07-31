import secrets
import ecdsa
import binascii

def sign_msg(private_key, msg):
    sk=ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
    vk=sk.verifying_key
    signature = sk.sign(msg)
    check_ret=vk.verify(signature, msg)
    print(check_ret)
    print("compress signature:" + vk.to_string("compressed").hex())
    print("uncompress signature:" + vk.to_string("uncompressed").hex())
    print("after sign:"+binascii.hexlify(signature).decode())
    return binascii.hexlify(signature).decode()

def verify_from_string(public_key, signed_msg, msg):
    vk = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key), curve=ecdsa.SECP256k1)
    print("compress signature:" + vk.to_string("compressed").hex())
    print("uncompress signature:" + vk.to_string("uncompressed").hex())
    try:
        ret = vk.verify(binascii.unhexlify(signed_msg), msg)
        print(ret)
        return True
    except:
        print("verify failed")
        return False

def gen_private_key():
    bits = secrets.randbits(256)
    return hex(bits)[2:]

def gen_public_by_private_key(private_key):
    signing_key = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
    pub = signing_key.get_verifying_key()

    #print("public key: " + binascii.hexlify(pub.to_string()).decode())
    return binascii.hexlify(pub.to_string()).decode()

def gen_private_and_public():
    private_key=gen_private_key()
    public_key=gen_public_by_private_key(private_key)
    return private_key, public_key
