import json
from datetime import datetime

import web3.eth
from web3 import Web3
import datetime
import argparse
import os

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 这个address是所部署合约的地址
with open('../contract.txt', 'r') as f:
    authensc_addr = f.read().replace('\n', '').replace('\r', '')
    f.close()
# authensc_addr = "0x85A4427A86872854AfC8152A77e94987eA526811"
#                 0xcdeDD3D2c582A1b961F211483ee3EebF612763d3

print(authensc_addr)

if os.path.exists('../pwd_admin.txt'):
    with open('../pwd_admin.txt', 'r') as f:
        pwd_admin = f.read().replace('\n', '').replace('\r', '')
        f.close()



print(pwd_admin)
print(type(pwd_admin))

with open('./accounts_list.txt', 'w+') as wf:

    for i in range(100):
        addr_line = "{\"id\": \"ship"
        tmp = str(i)
        if i < 10:
            tmp = "0" + tmp
        addr_line += tmp
        addr_line += "\", \"address\": \""
        addr_line += w3.eth.accounts[i+1]
        addr_line += "\"},\n"
        print(addr_line)
        wf.write(addr_line)

    f.close()
