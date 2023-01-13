import os
import json
import argparse

parser= argparse. ArgumentParser()
parser.add_argument("-devnum",type=int, help="the number of device you want ", default=100)
parser.add_argument("-adminnum", type=int, help="the number of admin-device you want ", default=1)
parser.add_argument("-outjson", type=str, help="the name of blockchain config json ", default='gen_zczs.json')
args= parser.parse_args()

super_number  = args.adminnum
user_number = args.devnum

# with open("pwd_admin.txt","w") as f:
#     pwd_super = input('the passowrd of admin node:')
#     f.write(pwd_super)
#     f.close()
#
# with open("pwd_user.txt","w") as f:
#     pwd_dev = input('the passowrd of device node:')
#     f.write(pwd_dev)
#     f.close()

gen_zczs = {'config': {'chainId': 20210616, 'homesteadBlock': 0, 'eip150Block': 0, 'eip155Block': 0, 'eip158Block': 0, 'byzantiumBlock': 0, 'constantinopleBlock': 0, 'petersburgBlock': 0, 'istanbulBlock': 0, 'ethash': {}}, 'coinbase': '0x0000000000000000000000000000000000000000', 'difficulty': '0x20000', 'extraData': '', 'gasLimit': '0xffffffff', 'nonce': '0x0000000000000042', 'mixhash': '0x0000000000000000000000000000000000000000000000000000000000000000', 'parentHash': '0x0000000000000000000000000000000000000000000000000000000000000000', 'timestamp': '0x00', 'alloc': {}}
id_addr = {'admin':[],'dev':[]}

for i in range(super_number):
    res = os.popen('geth --datadir ./adminnode/  account new --password pwd_admin.txt').readlines()
    addr_pz = {"balance": "1000000000000000000000"}
    addr = res[3][31:-1]
    gen_zczs['alloc'][addr] = addr_pz
    id_addr['admin'].append({'id': 'admin' + str(int(i/10)) + str(i%10), 'address' : '0x'+ addr})
    print(i, ' / ', super_number)

for i in range(user_number):
    res = os.popen('geth --datadir ./adminnode/  account new --password pwd_user.txt').readlines()
    addr_pz = { "balance": "1000000000000000000000" }
    addr = res[3][31:-1]
    gen_zczs['alloc'][addr] = addr_pz
    id_addr['dev'].append({'id': 'ship' + str(int(i/10)) + str(i%10), 'address' : '0x'+ addr})
    print(i,' / ',user_number)


with open(args.outjson,"w") as f:
     json.dump(gen_zczs,f)
     f.close()

with open("id-addr.json", "w") as f:
 json.dump(id_addr, f)
 f.close()

print("已生成",super_number+user_number,"个密钥，存储在keystore中")
print("区块链配置文件为:", args.outjson)





