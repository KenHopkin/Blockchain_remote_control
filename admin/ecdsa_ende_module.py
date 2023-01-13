import ecdsa
import os
import base64

# 系统初始配置时使用，读取pwd_user.txt文件，生成其对应的公钥，存储在pkforall.txt里。存储细节可以继续优化
def write_pk(pwd):
    # ----------------------------------------------------------------------------------
    address = '0xfdsafdsafs'
    #-----------------------------------------------------------------------------------
    pwd = pwd + address[-6:]
    seed = bytes(pwd, encoding='utf-8')
    secexp = ecdsa.util.randrange_from_seed__trytryagain(seed, ecdsa.SECP256k1.order)
    sk = ecdsa.SigningKey.from_secret_exponent(secexp, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    vk_byte = vk.to_string()

    with open('pkforall.txt', 'wb') as f:
        f.write(vk_byte)
        f.close()

    print(vk_byte)
    return vk_byte


#单块ecc加密逻辑，En = [kG, (H+kQ)mod(n)]
def ecc_en(vk, msg_int, k, r):
    G = vk.pubkey.generator
    n = G.order()
    Q = vk.pubkey
    msg_ed = (msg_int + (k * Q.point).x()) % n
    print("part: plainint", msg_int)
    print("part: cryptint", msg_ed)
    return (msg_ed)

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

#文本分块
def deal_text(msg_str, max_len):
    msgs = []
    while msg_str:
        input = bytes(msg_str[:max_len], encoding='UTF-8')
        msg_str = msg_str[max_len:]
        msgs.append(int.from_bytes(input, byteorder='big', signed=False))
    return msgs


#可处理分块的Ecc加密
def encrypt(msg, vk_byte):
    pk = ecdsa.VerifyingKey.from_string(vk_byte, curve=ecdsa.SECP256k1)
    max_len = ecdsa.SECP256k1.baselen
    msgs_ened_byte = b''

    G = pk.pubkey.generator
    k = ecdsa.util.randrange(ecdsa.SECP256k1.order)
    r = k * G
    r_byte = base64.b64encode(r.x().__int__().to_bytes(max_len, "big"))

    for i in deal_text(msg, max_len):
        msg_ened_int = ecc_en(pk, i, k, r)
        assert msg_ened_int > 0
        msg_ened_byte = msg_ened_int.__int__().to_bytes(max_len, "big")
        msgs_ened_byte += base64.b64encode(msg_ened_byte)
    encrypt_result = r_byte + msgs_ened_byte
    encrypt_result = encrypt_result.decode('ascii')
    print("plaintext is :", msg)
    print("encryptedtext is :", encrypt_result)
    return encrypt_result

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

