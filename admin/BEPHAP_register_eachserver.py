# from module import node_module
import copy
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
servers_dev = []
w3s = []
server_ips = []

if os.path.exists('pwd_user.txt'):
    with open('pwd_user.txt','r') as f:
        pwd = f.read().replace('\n', '').replace('\r', '')
        f.close()
else:
    pwd = input('please input the dev password: ')

# 部署合约后得到的ABI
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

def produce_complete_ip_web3(string_ip, hport):
    for port_suffix in range(4):
        server_ips.append(string_ip + str(hport+port_suffix))
        # print(string_ip + str(hport+port_suffix))

def init_servers_web3(ass_group, ass_leftind, ass_rightind):
    # cssc
    str_ip = "http://192.168.102.37:"
    http_port = 8545
    produce_complete_ip_web3(str_ip, http_port)

    # krace
    str_ip = "http://192.168.102.72:"
    http_port = 8545
    produce_complete_ip_web3(str_ip, http_port)

    # yu_jumper
    str_ip = "http://192.168.102.41:"
    http_port = 8545
    produce_complete_ip_web3(str_ip, http_port)

    # datacon
    str_ip = "http://192.168.102.43:"
    http_port = 8545
    produce_complete_ip_web3(str_ip, http_port)


    nodeIDs = dev_id[ass_leftind:(ass_rightind + 1)]
    print("nodeIDs: ", nodeIDs)
    task_id = ass_group
    authensc_list = []
    for each_ip in server_ips:
        dev_grp = []
        dev_grp.clear()
        w3s.append(Web3(Web3.HTTPProvider(each_ip)))
        authensc_list.append(w3s[-1].eth.contract(address=Web3.toChecksumAddress(authensc_addr),
                                   abi=abi_a))
        # print("when init:", each_ip)
        masteraddr = authensc_list[-1].functions.DomainInfo(ass_group).call()[1]
        master_id = dev_id[w3s[-1].eth.accounts.index(masteraddr)]

        dev_grp.append(
            node_module.Node(Web3(Web3.HTTPProvider(each_ip)), authensc_list[-1], master_id,
                             w3s[-1].eth.accounts[dev_id.index(master_id)]))
        dev_grp[-1].node_idx = dev_id.index(master_id)

        for nodeid in nodeIDs:
            dev_grp.append(
                node_module.Node(Web3(Web3.HTTPProvider(each_ip)), authensc_list[-1], nodeid,
                                 w3s[-1].eth.accounts[dev_id.index(nodeid)]))
            dev_grp[-1].node_idx = dev_id.index(nodeid)
        servers_dev.append(dev_grp)


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
        # time_authen1 = datetime.datetime.now()
        # print(device[i + 1].device_au(dev_id.index(nodeIDs[i]), task_id, nodeIDs[i], "Hello, I'm " + nodeIDs[i]))
        # time_authen2 = datetime.datetime.now()
        # print("无人艇发送数据 以及两个无人艇身份认证所需时间：", time_authen2 - time_authen1, "秒")


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

def servers_check_associate(ass_group, ass_leftind, ass_rightind):


    nodeIDs = dev_id[ass_leftind:(ass_rightind + 1)]
    onchaindev = []
    lossdev = []
    range_servers = list(range(len(w3s)))
    tmp_range = copy.deepcopy(range_servers)

    while len(range_servers) > 0:
        print("range_servers: ", range_servers)
        for i in range_servers:
            onchaindev.clear()
            lossdev.clear()
            for each in servers_dev[i]:
                curr_dm = each.dev_dm_iterate_start()
                while each.dev_dm_can_iterate(curr_dm):
                    onchaindev.append((curr_dm, each.id))
                    # print(curr_dm, each.id, device[i].query_lgtlttwh(curr_dm, each.id))
                    curr_dm = each.dev_dm_iterate_next(curr_dm)
            for nodeid in nodeIDs:
                if (ass_group, nodeid) not in onchaindev:
                    lossdev.append(nodeid)
            if len(lossdev) == 0:
                print(i, ": all device are on chain ")
                tmp_range.remove(i)
            else:
                print(i, ": loss devices:", lossdev)
        range_servers = copy.deepcopy(tmp_range)


if __name__ == "__main__":
    # gen_dev_id("vehicle", 1005)
    # associate_dev("thefirsttest", dev_id[5])
    # associate_multi_dev("thefirsttest",7,16)
    # check_associate("thefirsttest",7,16)
    # init_servers_web3("thefirsttest",7,16)
    ass_grp = "thefirsttest"
    start_dev = 81
    end_dev = 130  # included
    init_servers_web3(ass_grp, start_dev, end_dev)
    w3s[0].geth.miner.start(2)
    time_add_device1 = datetime.datetime.now()
    associate_multi_dev(ass_grp, start_dev, end_dev)
    servers_check_associate(ass_grp, start_dev, end_dev)
    time_add_device2 = datetime.datetime.now()
    w3s[0].geth.miner.stop()
    result_str = "add device number " + str(end_dev-start_dev+1) + ", cost time:" \
                 + str(time_add_device2 - time_add_device1) + "秒 \n" + "each is " \
                 + str((time_add_device2 - time_add_device1)/(end_dev-start_dev+1)) + "\n"
    print("add device number ", end_dev-start_dev+1, ", cost time:", (time_add_device2 - time_add_device1), "秒")
    with open("experiment_register.txt", 'a+') as register_result:
        register_result.write(result_str)



