# from module import node_module
import json

from web3 import Web3
import datetime
import node_module
import argparse
import os

# massage  sender




dev_ip = 'http://127.0.0.1:8545'
dev_id = ['admin00','ship00','ship01','ship02','ship03','ship04','ship05','ship06','ship07','ship08','ship09','ship10','ship11','ship12','ship13','ship14','ship15','ship16','ship17','ship18','ship19']
#dev_id = ['', 'ship11','ship12','ship13','ship14','ship15','ship21','ship22']
device = []

if os.path.exists('pwd_user.txt'):
    with open('pwd_user.txt','r') as f:
        pwd = f.read().replace('\n', '').replace('\r', '')
        f.close()
else:
    pwd = input('please input the dev password: ')

# 部署合约后得到的ABI
#abi_a = [{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AssociationPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AssociationVerifyDeviceSig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"AssociationVerifyMasterSig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AthenticationPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"},{"internalType":"bytes","name":"DeviceSig","type":"bytes"}],"name":"AthenticationVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"master_id","type":"string"},{"internalType":"string","name":"DomainID","type":"string"}],"name":"BuildDomain","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"master_id","type":"string"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"BuildPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"BuildVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"Buildflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"}],"name":"DataInteract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"DeviceCert","outputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes32","name":"MsgHash","type":"bytes32"},{"internalType":"bytes","name":"Sig","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"DomainInfo","outputs":[{"internalType":"bool","name":"IsUsed","type":"bool"},{"internalType":"address","name":"MasterAddr","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"GetAssociationHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"string","name":"Data","type":"string"}],"name":"GetAthenticationHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"}],"name":"GetBuildHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"}],"name":"GetCertHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"deviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"}],"name":"GetManageHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"}],"name":"LenDomainInfoDevice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"}],"name":"LenDomainInfoDeviceData","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"}],"name":"LenMasterDomain","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"Maflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"}],"name":"Manage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"ManageVerifySig","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"int8","name":"flag","type":"int8"},{"internalType":"bytes","name":"MasterSig","type":"bytes"}],"name":"ManagementPhase","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"MasterDomain","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"}],"name":"Register","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"ResetAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"MasterAddr","type":"address"},{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"bytes32","name":"MsgHash","type":"bytes32"},{"internalType":"bytes","name":"Sig","type":"bytes"}],"name":"SendCert","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"DeviceAddr","type":"address"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewCertByAddr","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewData","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"string","name":"DeviceID","type":"string"}],"name":"ViewDeviceByID","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"DomainID","type":"string"},{"internalType":"uint256","name":"i","type":"uint256"}],"name":"ViewDeviceByIndex","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"int8","name":"","type":"int8"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"assflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"authflag","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"message","type":"bytes32"},{"internalType":"bytes","name":"sig","type":"bytes"}],"name":"recoverSigner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"}]
with open('contract_ABI.json', 'r') as abi_f:
    abi_a = json.load(abi_f)

# 这个address是所部署合约的地址
with open('contract.txt', 'r') as f:
    authensc_addr= f.read().replace('\n', '').replace('\r', '')
    f.close()

# authensc_addr = "0x4670E1725991756820b8eE55B7b27D710B7770Fc"

def gen_dev_id(prefix, gen_number):
    for i in range(gen_number):

        suffix = str(i).zfill(4)
        dev_name = prefix + suffix

        dev_id.append(dev_name)
    print(dev_id)

gen_dev_id("vehicle", 1005)

def init_web3_dev(ass_group, ass_leftind, ass_rightind):
    # 用HTTP连接三个节点
    w3 = Web3(Web3.HTTPProvider(dev_ip))

    nodeIDs = dev_id[ass_leftind:(ass_rightind + 1)]
    task_id = ass_group

    # tmp_addr = '0xcdeDD3D2c582A1b961F211483ee3EebF612763d3'
    authensc = w3.eth.contract(address=Web3.toChecksumAddress(authensc_addr),
                               abi=abi_a)
    masteraddr = authensc.functions.DomainInfo(ass_group).call()[1]
    master_id = dev_id[w3.eth.accounts.index(masteraddr)]

    device.append(
        node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, master_id,
                         w3.eth.accounts[dev_id.index(master_id)]))
    device[-1].node_idx = dev_id.index(master_id)

    for nodeid in nodeIDs:
        device.append(
            node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, nodeid, w3.eth.accounts[dev_id.index(nodeid)]))
        device[-1].node_idx = dev_id.index(nodeid)


def associate_dev(ass_group, ass_node):
    # parser = argparse.ArgumentParser()

    # parser.add_argument("-group", help="group to join", default="Task01", required=True)
    # parser.add_argument("-node", help="devID", default="ship01", required=True)
    # args = parser.parse_args()
    # # args = argparse.Namespace(group= 'Task01', node = 'ship13')


    # 用HTTP连接三个节点
    w3 = Web3(Web3.HTTPProvider(dev_ip))
    device = []

    authensc = w3.eth.contract(address=Web3.toChecksumAddress(authensc_addr),
                               abi=abi_a)

    masteraddr = authensc.functions.DomainInfo(ass_group).call()[1]

    device.append(
        node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, '',
                         masteraddr))
    device.append(
        node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, ass_node,
                         w3.eth.accounts[dev_id.index(ass_node)]))

    # sign cert
    device[0].mas_create_other_cert(device[1], ass_group)

    time_add_device1 = datetime.datetime.now()
    print(device[1].device_association(0, dev_id.index(ass_node)))
    time_add_device2 = datetime.datetime.now()
    print("无人艇加入信任域所需时间：", (time_add_device2 - time_add_device1), "秒")

def associate_multi_dev(ass_group, ass_leftind, ass_rightind):
    # 用HTTP连接三个节点
    w3 = Web3(Web3.HTTPProvider(dev_ip))


    nodeIDs = dev_id[ass_leftind:(ass_rightind+1)]
    task_id = ass_group

    # tmp_addr = '0xcdeDD3D2c582A1b961F211483ee3EebF612763d3'
    authensc = w3.eth.contract(address=Web3.toChecksumAddress(authensc_addr),
                               abi=abi_a)
    masteraddr = authensc.functions.DomainInfo(ass_group).call()[1]
    master_id = dev_id[w3.eth.accounts.index(masteraddr)]

    device.append(
        node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, master_id,
                         w3.eth.accounts[dev_id.index(master_id)]))
    device[-1].node_idx = dev_id.index(master_id)

    for nodeid in nodeIDs:
        device.append(
            node_module.Node(Web3(Web3.HTTPProvider(dev_ip)), authensc, nodeid, w3.eth.accounts[dev_id.index(nodeid)]))
        device[-1].node_idx = dev_id.index(nodeid)

    # device[0].mas_rst_contract2(w3.eth.accounts[dev_id.index(master_id)])

    # sign cert
    for i in range(len(nodeIDs)):
        device[0].mas_create_other_cert(device[i + 1], task_id)

    # time_start = datetime.datetime.now()
    # print(device[0].mas_build_domain(master_id, task_id))
    # time_build_domain = datetime.datetime.now()
    # print("创建信任域所需时间：", (time_build_domain - time_start), "秒")

    for i in range(len(nodeIDs)):
        time_add_device1 = datetime.datetime.now()
        print(device[i + 1].device_association(0, dev_id.index(nodeIDs[i])))
        time_add_device2 = datetime.datetime.now()
        print(dev_id[i] + "无人艇加入信任域所需时间：", (time_add_device2 - time_add_device1), "秒")
        time_authen1 = datetime.datetime.now()
        print(device[i + 1].device_au(dev_id.index(nodeIDs[i]), task_id, nodeIDs[i], "Hello, I'm " + nodeIDs[i]))
        time_authen2 = datetime.datetime.now()
        print("无人艇发送数据 以及两个无人艇身份认证所需时间：", time_authen2 - time_authen1, "秒")


def check_associate(ass_group, ass_leftind, ass_rightind):
    init_web3_dev(ass_group, ass_leftind, ass_rightind)
    nodeIDs = dev_id[ass_leftind:(ass_rightind + 1)]
    onchaindev = []
    lossdev = []
    for each in device:
        curr_dm = each.dev_dm_iterate_start()
        while each.dev_dm_can_iterate(curr_dm):
            onchaindev.append((curr_dm, each.id))
            # print(curr_dm, each.id, device[i].query_lgtlttwh(curr_dm, each.id))
            curr_dm = each.dev_dm_iterate_next(curr_dm)
    for nodeid in nodeIDs:
        if (ass_group, nodeid) not in onchaindev :
            lossdev.append(nodeid)
    if len(lossdev) == 0:
        print("all device are on chain")
        return True
    else:
        print("loss devices:", lossdev)
        return False

if __name__ == "__main__":
    # gen_dev_id("vehicle", 1005)
    # associate_dev("thefirsttest", dev_id[5])
    # associate_multi_dev("thefirsttest",7,16)
    check_associate("thefirsttest",7,16)




