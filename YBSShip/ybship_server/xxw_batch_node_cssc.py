# -*- coding: utf-8 -*-
import copy

import remote_node_module
from sshlib import *
from httplib import *
from web3 import Web3
import time
import os
import random
import multiprocessing

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


    for j in range(len(rnode_list)):


        i = len(rnode_list) - j - 1
        plists.append(multiprocessing.Process(target=restart_geth, args=(rnode_list[i].ssh_info,
                                                                         rnode_list[i].sh_local_path,
                                                                         rnode_list[i].sh_remote_path,
                                                                         rnode_list[i].node_folder_path,
                                                                         rnode_list[i].node_name)))

        plists[-1].start()
        plists[-1].join(5)
        print("link node in ", rnode_list[i].web3http)
        # time.sleep(10)

        w3_list.append(Web3(Web3.HTTPProvider(rnode_list[i].web3http)))
        print('nodeInfo: ', w3_list[-1].eth.blockNumber)
        plists[-1].terminate()


