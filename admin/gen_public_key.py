import ecdsa
import os
import base64

pk_ls = []


def write_every_pk(pwd, i):

    # ----------------------------------------------------------------------------------
    address = '0xfdsafdsafs'
    #-----------------------------------------------------------------------------------
    pwd = pwd + address[-6:]
    seed = bytes(pwd, encoding='utf-8')
    secexp = ecdsa.util.randrange_from_seed__trytryagain(seed, ecdsa.SECP256k1.order)
    sk = ecdsa.SigningKey.from_secret_exponent(secexp, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    vk_byte = vk.to_string()

    pk_path = "./public_key/" + str(i) + ".txt"

    with open(pk_path, 'wb') as f:
        f.write(vk_byte)
        f.close()

    print(vk_byte)
    pk_ls.append(vk_byte)
    return vk_byte



for number in range(101):
    # the secret key of ship12 is "mima12"
    pwd = "mima" + str(number)
    print(pwd)
    write_every_pk(pwd, number)