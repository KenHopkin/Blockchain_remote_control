import json
from datetime import datetime
#from module import node_module
from web3 import Web3
import node_module
import argparse
import os

# massage  sender

parser = argparse.ArgumentParser()

parser.add_argument("-group", help="group to send", default="Task01", required=True)
parser.add_argument("-master",help="masterID", default="ship00", required=True)
parser.add_argument("-other",help="otherID", default="ship01", required=True)
args = parser.parse_args()


dev_ip = 'http://127.0.0.1:8545'
dev_id = ['admin00','ship00','ship01','ship02','ship03','ship04','ship05','ship06','ship07','ship08','ship09','ship10','ship11','ship12','ship13','ship14','ship15','ship16','ship17','ship18','ship19']
# dev_id = ['', 'ship11','ship12','ship13','ship14','ship15','ship21','ship22']

if os.path.exists('pwd_admin.txt'):
    with open('pwd_admin.txt','r') as f:
        pwd = f.read().replace('\n', '').replace('\r', '')
        f.close()
else:
    pwd = input('please input the password: ')

# 部署合约后得到的ABI
#abi_a = [{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AssociationPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AssociationVerifyDeviceSig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"AssociationVerifyMasterSig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AthenticationPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AthenticationVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"MasterID","type":"string"},{"internalType":"string","name":"DomainID","type":"string"}],"name":"BuildDomain","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"MasterID","type":"string"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"BuildPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"BuildVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"Buildflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"}],"name":"DataInteract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"DeviceCert","outputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes32","name":"MsgHash","type":"bytes32"},{"internalType":"bytes","name":"Sig","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"DomainInfo","outputs":[{"internalType":"bool","name":"IsUsed","type":"bool"},{"internalType":"address","name":"MasterAddr","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"GetAssociationHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"}],"name":"GetAthenticationHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"}],"name":"GetBuildHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"}],"name":"GetCertHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"deviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"}],"name":"GetManageHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"}],"name":"LenDomainInfoDevice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"}],"name":"LenDomainInfoDeviceData","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"}],"name":"LenMasterDomain","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"Maflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"}],"name":"Manage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"ManageVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"ManagementPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"MasterDomain","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"}],"name":"Register","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"ResetAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes32","name":"MsgHash","type":"bytes32"},{"internalType":"bytes","name":"Sig","type":"bytes"}],"name":"SendCert","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewCertByAddr","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewData","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"}],"name":"ViewDeviceByID","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewDeviceByIndex","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"assflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"authflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"message","type":"bytes32"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"recoverSigner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"}]
with open('contract_ABI.json', 'r') as abi_f:
    abi_a = json.load(abi_f)

# 这个address是所部署合约的地址
with open('contract.txt', 'r') as f:
    authensc_addr= f.read().replace('\n', '').replace('\r', '')
    f.close()
# authensc_addr = "0xC3AF15d40cB1D059b1C0289Caea555b7b2944db3"


if __name__ == "__main__":
    # 用HTTP连接三个节点
    w3 = Web3(Web3.HTTPProvider(dev_ip))
    device = []

    authensc = w3.eth.contract(address=Web3.toChecksumAddress(authensc_addr),
                                  abi=abi_a)

    device.append(
        node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, args.master,
                         w3.eth.accounts[dev_id.index(args.master)]))
    # sign cert
    fault_addr = w3.eth.accounts[dev_id.index(args.other)]
    print(device[0].fault_build_domain(args.master, fault_addr, args.group))

















