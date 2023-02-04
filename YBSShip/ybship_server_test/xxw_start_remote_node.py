# -*- coding: utf-8 -*-
from sshlib import *
from httplib import *
from web3 import Web3
import time
import os
import random

keyfiles = [ keyfile for keyfile in os.listdir("/home/cssc/Documents/workspace/adminnode/keystore") if ("UTC" in keyfile)]
Ipdata = []

sshinfo = {
	'host':'0.0.0.0',
	'port': 22,
	'username': 'cssc',
	'password': 'cssc123'
}

sshinfo_krace = {
	'host':'192.168.102.44',
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
	client.connect()

	# 上传秘钥文件
	# client.upload('./gen_zczs.json', '/home/cssc/Documents/workspace/devnode/gen_zczs.json')
	# client.upload('/home/cssc/Documents/workspace/adminnode/keystore/' + keyfiles[idx], '/home/cssc/Documents/workspace/devnode/keystore/'+keyfiles[idx])
	client.upload(run_cmd_path, target_path)
	# 启动/重启gethssss
	data = client.run_cmd("ps aux|grep geth|awk '{print $2}'|xargs kill")['res']
	print(data)
	data = client.run_cmd('cd /home/cssc/Documents/workspace && geth --datadir devnode init gen_zczs.json')['res']
	data = client.run_cmd('cd ' + target_folder +' && geth --datadir ' + nodename +' init gen_zczs.json')['res']

	print("[2]", data)
	# data = client.run_cmd('cd /home/cssc/Documents/workspace && nohup geth --http --http.corsdomain="*" --http.api web3,eth,debug,personal,net,txpool,admin --http.addr=0.0.0.0 --vmdebug --datadir devnode  --allow-insecure-unlock --nodiscover > log 2>&1 &')['res']
	data = client.run_cmd("cd " + target_folder +" && chmod +x run_" + nodename + ".sh && ./run_" + nodename + ".sh")
	print("[3]", data)
	# 关闭连接
	client.close()


if __name__ == '__main__':
	node_name = 'exnode01'
	run_exnode01_path = '/home/cssc/Documents/workspace/uptodate/blockchain_node_control/YBSShip/ybship_server_test/run_exnode01.sh'
	exnode01_target_path = '/home/' + sshinfo_krace['username'] + '/Documents/iov_BC_experiment/run_' + node_name + '.sh'
	target_folder_path = '/home/' + sshinfo_krace['username'] + '/Documents/iov_BC_experiment'
	restart_geth(sshinfo_krace, run_exnode01_path, exnode01_target_path, target_folder_path, node_name)