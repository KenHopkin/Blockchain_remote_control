import json
from datetime import datetime
import admin.node_module as node_module
from web3 import Web3
import datetime
import argparse
import os
import math

# massage  sender

parser = argparse.ArgumentParser()

parser.add_argument("-node",help="nodeID", default="ship01, ship02, ship03, ship04", nargs='+')
parser.add_argument("-longitude",help="longitude", default="114", nargs='+')
parser.add_argument("-latitude",help="latitude", default="12", nargs='+')


args = parser.parse_args()
#args = argparse.Namespace(group= 'Task11', master = 'ship11', node = 'ship12  ship13')


dev_ip = 'http://127.0.0.1:8545'
# dev_ip = 'http://159.226.94.155:8080'

dev_id = ['admin00','ship00','ship01','ship02','ship03','ship04','ship05','ship06','ship07','ship08','ship09','ship10','ship11','ship12','ship13','ship14','ship15','ship16','ship17','ship18','ship19']
# dev_id = ['', 'ship11','ship12','ship13','ship14','ship15']

if os.path.exists('pwd_admin.txt'):
    with open('pwd_admin.txt','r') as f:
        pwd_admin = f.read().replace('\n', '').replace('\r', '')
        f.close()
else:
    pwd_admin = input('please input the password of admin: ')

if os.path.exists('pwd_user.txt'):
    with open('pwd_user.txt','r') as f:
        pwd_dev = f.read().replace('\n', '').replace('\r', '')
        f.close()
else:
    pwd_dev = input('please input the password of device: ')

# 部署合约后得到的ABI
# abi_a = [{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AssociationPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AssociationVerifyDeviceSig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"AssociationVerifyMasterSig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AthenticationPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AthenticationVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"MasterID","type":"string"},{"internalType":"string","name":"DomainID","type":"string"}],"name":"BuildDomain","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"MasterID","type":"string"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"BuildPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"BuildVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"Buildflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"}],"name":"DataInteract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"DeviceCert","outputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes32","name":"MsgHash","type":"bytes32"},{"internalType":"bytes","name":"Sig","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"DomainInfo","outputs":[{"internalType":"bool","name":"IsUsed","type":"bool"},{"internalType":"address","name":"MasterAddr","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"GetAssociationHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"}],"name":"GetAthenticationHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"}],"name":"GetBuildHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"}],"name":"GetCertHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"deviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"}],"name":"GetManageHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"}],"name":"LenDomainInfoDevice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"}],"name":"LenDomainInfoDeviceData","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"}],"name":"LenMasterDomain","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"Maflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"}],"name":"Manage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"ManageVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"ManagementPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"MasterDomain","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"}],"name":"Register","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"ResetAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes32","name":"MsgHash","type":"bytes32"},{"internalType":"bytes","name":"Sig","type":"bytes"}],"name":"SendCert","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewCertByAddr","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewData","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"}],"name":"ViewDeviceByID","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewDeviceByIndex","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"assflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"authflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"message","type":"bytes32"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"recoverSigner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"}]
with open('contract_ABI.json', 'r') as abi_f:
    abi_a = json.load(abi_f)

# 这个address是所部署合约的地址
with open('contract.txt', 'r') as f:
    authensc_addr = f.read().replace('\n', '').replace('\r', '')
    f.close()
#authensc_addr = "0x85A4427A86872854AfC8152A77e94987eA526811"
#                 0xcdeDD3D2c582A1b961F211483ee3EebF612763d3

nodeID = args.node[0]

lgt = args.longitude[0]
ltt = args.latitude[0]


if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider(dev_ip))
    device = []
    authensc = w3.eth.contract(address=Web3.toChecksumAddress(authensc_addr),
                               abi=abi_a)
    device.append(
        node_module.Node(
            Web3(Web3.HTTPProvider(dev_ip)), authensc, args.node,
            w3.eth.accounts[dev_id.index(nodeID)]))
    # print(dev_ip, device[-1].id, device[-1].addr)
    device[0].node_idx = dev_id.index(nodeID)
    print(type(nodeID))
    print(type(lgt), lgt)
    # curr_leader = device[0].query_dm_leader(task_id)
    # device.append(
    #     node_module.Node(
    #         Web3(Web3.HTTPProvider(dev_ip)), authensc, dev_id[w3.eth.accounts.index(curr_leader)],curr_leader))
    curr_dm = device[0].dev_dm_iterate_start()
    (curr_lgt, curr_ltt) = device[0].query_lgtltt(curr_dm, nodeID)

    # device[0].lgt = lgt
    # device[0].ltt = ltt

    clgt = float(curr_lgt)
    cltt = float(curr_ltt)
    tarlgt = float(lgt)
    tarltt = float(ltt)

    interval = 1

    while (math.fabs(clgt - tarlgt) > interval) or (math.fabs(cltt - tarltt) > interval):
        if math.fabs(clgt - tarlgt) > interval:
            if clgt > tarlgt:
                clgt = clgt - interval
            else:
                clgt = clgt + interval

        if math.fabs(cltt - tarltt) > interval:
            if cltt > tarltt:
                cltt = cltt - interval
            else:
                cltt = cltt + interval
        print(clgt, cltt)
        device[0].lgt = str(clgt)
        device[0].ltt = str(cltt)
        device[0].update_heartbeat()

    device[0].lgt = lgt
    device[0].ltt = ltt
    device[0].update_heartbeat()


