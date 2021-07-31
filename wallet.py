import Core.secure as secure

priv=secure.gen_private_key()
print(priv)

priv_key, pub_key = secure.gen_private_and_public()
print("private_key: " + priv_key)
print("public_key: " + pub_key)
