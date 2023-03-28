# -*- coding: utf-8 -*-
import copy

import requests
import urllib3

import remote_node_module
from sshlib import *
from httplib import *
from web3 import Web3
import time
import os
import random
import multiprocessing
import json
import os

keyfiles = [keyfile for keyfile in os.listdir("./keystore") if ("UTC" in keyfile)]
Ipdata = []
sshinfo_list = []

sshinfo = {
    'host': '0.0.0.0',
    'port': 22,
    'username': 'cssc',
    'password': 'cssc123'
}

sshinfo_krace = {
    'host': '192.168.102.44',
    'port': 22,
    'username': 'krace',
    'password': 'sklois123'
}


def write_list_to_json(list, json_file_name, json_file_save_path):
    """
    将list写入到json文件
    :param list:
    :param json_file_name: 写入的json文件名字
    :param json_file_save_path: json文件存储路径
    :return:
    """
    os.chdir(json_file_save_path)
    with open(json_file_name, 'w') as  f:
        json.dump(list, f)



def restart_geth(ssh_info, run_cmd_path, target_path, target_folder, nodename):
    # ip = ssh_info['host']
    print("Handling " + ssh_info['host'])
    # 开启连接
    # sshinfo['host'] = ip
    client = SSHConnection(ssh_info)
    try:
        client.connect()
    except paramiko.SSHException:
        print("ssh 连接失败")
        return 0

    # 上传秘钥文件
    # client.upload('./gen_zczs.json', '/home/cssc/Documents/workspace/devnode/gen_zczs.json')
    # client.upload('/home/cssc/Documents/workspace/adminnode/keystore/' + keyfiles[idx], '/home/cssc/Documents/workspace/devnode/keystore/'+keyfiles[idx])
    client.upload(run_cmd_path, target_path)
    # 启动/重启gethssss
    data = client.run_cmd("ps aux|grep geth|awk '{print $2}'|xargs kill")['res']
    print(data)
    data = client.run_cmd("pkill geth")['res']
    print(data)
    # data = client.run_cmd('cd /home/cssc/Documents/workspace && geth --datadir devnode init gen_zczs.json')['res']
    data = client.run_cmd('cd ' + target_folder + ' && geth --datadir ' + nodename + ' init gen_zczs.json')['res']

    print("[2]", data)
    # data = client.run_cmd('cd /home/cssc/Documents/workspace && nohup geth --http --http.corsdomain="*" --http.api web3,eth,debug,personal,net,txpool,admin --http.addr=0.0.0.0 --vmdebug --datadir devnode  --allow-insecure-unlock --nodiscover > log 2>&1 &')['res']
    data = client.run_cmd("cd " + target_folder + " && chmod +x run_" + nodename + ".sh && ./run_" + nodename + ".sh")
    # data = client.run_cmd("cd " + target_folder +" && chmod +x run_" + nodename + ".sh && nohup ./run_" + nodename + ".sh")
    # commandgethstart = "cd " + target_folder +" && chmod +x run_" + nodename + ".sh && nohup ./run_" + nodename + ".sh"
    # print(type(commandgethstart), "length: ", len(commandgethstart))
    # pn = multiprocessing.Process(target=client.run_cmd, args=(commandgethstart,))
    # pn.start()
    print("[3]", data)
    # print("link successfully\n")
    # time.sleep(10)
    # 关闭连接
    client.close()
    time.sleep(5)




def connect_nodes(ssh_info, run_cmd_path, target_path):

    print("Handling " + ssh_info['host'])
    # 开启连接
    # sshinfo['host'] = ip
    client = SSHConnection(ssh_info)
    try:
        client.connect()
    except paramiko.SSHException:
        print("ssh 连接失败")
        return 0

    # 上传秘钥文件
    # client.upload('./gen_zczs.json', '/home/cssc/Documents/workspace/devnode/gen_zczs.json')
    # client.upload('/home/cssc/Documents/workspace/adminnode/keystore/' + keyfiles[idx], '/home/cssc/Documents/workspace/devnode/keystore/'+keyfiles[idx])
    print("upload %s to %s" %(run_cmd_path, target_path))
    client.upload(run_cmd_path, target_path)

    client.close()
    time.sleep(5)



if __name__ == '__main__':
    plists = []
    rnode_list = []
    w3_list = []

    # 获取ip
    tmpsshinfo = {
        'host': '0.0.0.0',
        'port': 22,
        'username': 'cssc',
        'password': 'cssc123'
    }

    tmpsshinfo['host'] = '192.168.10.226'
    sshinfo_list.append(copy.deepcopy(tmpsshinfo))
    for i in range(25):

        if i < 5:
            tmpsshinfo['host'] = '192.168.10.'+str(231+i)
        else:
            tmpsshinfo['host'] = '192.168.10.'+str(201+i)
        # print(tmpsshinfo['host'])
        sshinfo_list.append(copy.deepcopy(tmpsshinfo))

    print(sshinfo_list)

    for i in range(len(sshinfo_list)):
        if i ==0 :
            rnode_list.append(remote_node_module.RNode(sshinfo_list[i], 'adminnode',
                                                       '/home/cssc/Documents/workspace',
                                                       './run_adminnode.sh',
                                                       '/home/cssc/Documents/workspace/run_' + 'adminnode' + '.sh',
                                                       'http://' + sshinfo_list[i]['host']+':'+str(8545)))
        else:
            for j in range(4):
                if j == 0:
                    tmpname = 'devnode'
                else:
                    tmpname = 'devnode' + str(j+1)
                rnode_list.append(remote_node_module.RNode(sshinfo_list[i], tmpname,
                                                           '/home/cssc/Documents/workspace',
                                                           './run_' + tmpname + '.sh',
                                                           '/home/cssc/Documents/workspace/run_' + tmpname + '.sh',
                                                           'http://' + sshinfo_list[i]['host']+':'+str(8545+j)))

    for i in range(len(rnode_list)):
        rnode_list[i].print()

    rnode_offlist = copy.deepcopy(rnode_list)

    # try:
    #     w3test = Web3(Web3.HTTPProvider('http://192.168.10.123:8545'))
    #     print(w3test.eth.blockNumber)
    # except requests.exceptions.ConnectTimeout:
    #     print("hahaha, I catched the fault")

    error_nodes = []

    # str_ip = []
    # str_ip.append("asdfafds4654")
    # str_ip.append("asdfk9999999999999000000000000000")
    #
    # write_list_to_json(str_ip, 'static-nodes', './')
    with open("./static-nodes.json","r") as load_f_l:
        rnode_enodes = json.load(load_f_l)

    with open("./xxw_batch_node_config.json","r") as load_f:
        loaddict = json.load(load_f)
        tmpstartindex = loaddict['start']

    for j in range(len(rnode_list))[tmpstartindex:]:

        print("j is ", j)


        tmpstartindex = loaddict['start']
        i = len(rnode_list) - j - 1
        print("start node in ", rnode_list[i].web3http)
        restart_geth(rnode_list[i].ssh_info, rnode_list[i].sh_local_path, rnode_list[i].sh_remote_path,
                     rnode_list[i].node_folder_path, rnode_list[i].node_name)

        # time.sleep(10)

        try:
            w3_list.append(Web3(Web3.HTTPProvider(rnode_list[i].web3http)))
            # print('nodeInfo: ', w3_list[-1].eth.blockNumber)
            target_info = w3_list[-1].geth.admin.nodeInfo()
            target_peer = target_info["enode"].replace("127.0.0.1", rnode_list[i].ssh_info['host'])
            rnode_enodes.append(target_peer)
            print(target_peer)
            loaddict['start'] = j+1
            with open("./xxw_batch_node_config.json","w") as load_f:
                json.dump(loaddict, load_f)
            write_list_to_json(rnode_enodes, 'static-nodes.json', './')

        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError, ConnectionAbortedError, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError):
            error_nodes.append(rnode_list[i])
            print("Error: node in %s can't link" % rnode_list[i].web3http)
            continue


    rnode_quchong = [item for item in rnode_enodes if rnode_enodes.count(item) == 1]
    write_list_to_json(rnode_quchong, 'static-nodes.json', './')

    for i in range(len(rnode_list)):
        print("start connect nodes, i = ", i)

        connect_nodes(rnode_list[i].ssh_info, './static-nodes.json', rnode_list[i].node_folder_path+'/'+rnode_list[i].node_name +'/static-nodes.json')
        print("start node in ", rnode_list[i].web3http)
        restart_geth(rnode_list[i].ssh_info, rnode_list[i].sh_local_path, rnode_list[i].sh_remote_path,
                     rnode_list[i].node_folder_path, rnode_list[i].node_name)