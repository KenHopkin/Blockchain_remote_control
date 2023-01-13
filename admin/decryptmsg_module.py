import ecdsa
import os
import base64

# 解密时调用，用于kG的恢复，减少存储空间。
def get_point_from_x(x):
    alpha = (pow(x, 3, ecdsa.SECP256k1.curve.p()) + (ecdsa.SECP256k1.curve.a() * x) + ecdsa.SECP256k1.curve.b()) % ecdsa.SECP256k1.curve.p()
    beta = ecdsa.numbertheory.square_root_mod_prime(alpha, ecdsa.SECP256k1.curve.p())
    y = beta if beta % 2 == 0 else ecdsa.SECP256k1.curve.p() - beta
    r = ecdsa.ellipticcurve.PointJacobi(ecdsa.SECP256k1.curve, x, y, 1, ecdsa.SECP256k1.order)
    return r


#单块ecc解密逻辑，De = (En - kG*d)mod(n)
def ecc_ed(sk, msg_ened_int, r):
    msg_re_int = (msg_ened_int - (sk.privkey.secret_multiplier * r).x()) % ecdsa.SECP256k1.order
    print("part: cryptint", msg_ened_int)
    print("part: plainint", msg_re_int)
    return  msg_re_int


#可处理分块的Ecc解密
def decrypt(encrypt_result, pwd):
    msgs_ened_str = encrypt_result
    # ----------------------------------------------------------------------------------
    address = '0xfdsafdsafs'
    #-----------------------------------------------------------------------------------
    pwd = pwd + address[-6:]
    seed = bytes(pwd, encoding='utf-8')
    secexp = ecdsa.util.randrange_from_seed__trytryagain(seed, ecdsa.SECP256k1.order)
    sk = ecdsa.SigningKey.from_secret_exponent(secexp, curve=ecdsa.SECP256k1)
    max_len = ecdsa.SECP256k1.baselen

    part = int(len(encrypt_result)/44)
    r_flag  =True
    r = 0
    msgs_re = []
    for i in range(part):
        msg_ened_str = msgs_ened_str[i*44:(i+1)*44]
        msg_ened_byte = base64.b64decode(msg_ened_str)
        msg_ened_int = int.from_bytes(msg_ened_byte, byteorder='big', signed=False)
        if r_flag == True:
            r_flag = False
            r = get_point_from_x(msg_ened_int)
        else:
            msg_int = ecc_ed(sk, msg_ened_int, r)
            msgs_re.append(msg_int.__int__().to_bytes(max_len, "big"))
    msgs_re_byte = b''.join(msgs_re)
    msgs_re_str = str(msgs_re_byte, encoding='UTF-8')
    print("plaintext is :",msgs_re_str)
    return msgs_re_str