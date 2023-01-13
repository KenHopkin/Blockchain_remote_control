# -*- coding: utf-8 -*-
from sshlib import *
from httplib import *
from web3 import Web3
import time
import os
import random

keyfiles = [ keyfile for keyfile in os.listdir("/home/cssc/Documents/workspace/adminnode/keystore") if ("UTC" in keyfile)]
Ipdata = []

init_adjmatrix = [
	[0,1,1,1,0,0,0,0,0],
	[1,0,0,0,0,0,1,0,0],
	[1,0,0,0,0,1,0,0,0],
	[1,0,0,0,1,1,1,0,0],
	[0,0,0,1,0,1,1,0,0],
	[0,0,1,1,1,0,0,0,1],
	[0,1,0,1,1,0,0,1,0],
	[0,0,0,0,0,0,1,0,0],
	[0,0,0,0,0,1,0,0,0],
]

# init_adjmatrix=[[0]]
# init_adjmatrix=[[0, 1],[1, 0]]
# 开始接收所有IP
ips = multiprocessing.Manager().list([])
main_p = multiprocessing.Process(target=ReveiveIPs, args=(ips,))
main_p.start()

sshinfo = {
	'host':'0.0.0.0',
	'port': 22,
	'username': 'cssc',
	'password': 'cssc123'
}
# 记录已经启动geth
recodes = []
# 记录已经处理peer连接
toporecodes = []

# 开始执行按照规划启动节点geth
while True:
	# 去重
	tempIpdata = list(set(ips[:]))
	with open("ipdata.txt","w") as f:
		f.writelines("\n".join(tempIpdata))
	# time.sleep(2)

	# 如果设备小于9和大于100都不处理
	if len(tempIpdata) > 100 or len(tempIpdata) < 9:
		print("Too much/few devices...")
		time.sleep(5)
		continue

	# 初始化节点
	for idx, ip in enumerate(tempIpdata):
		# 已经处理的跳过
		if ip in recodes:
			continue
		print("Handling " + ip)
		# 开启连接
		sshinfo['host'] = ip
		client = SSHConnection(sshinfo)
		client.connect()

		# 上传秘钥文件
		# client.upload('./gen_zczs.json', '/home/cssc/Documents/workspace/devnode/gen_zczs.json')
		# client.upload('/home/cssc/Documents/workspace/adminnode/keystore/' + keyfiles[idx], '/home/cssc/Documents/workspace/devnode/keystore/'+keyfiles[idx])
		client.upload("/home/cssc/Documents/workspace/YBSShip/ybship_server/run.sh", '/home/cssc/Documents/workspace/run.sh')

		# 启动/重启gethssss
		data = client.run_cmd("ps aux|grep geth|awk '{print $2}'|xargs kill")['res']
		print(data)
		data = client.run_cmd('cd /home/cssc/Documents/workspace && geth --datadir devnode init gen_zczs.json')['res']
		print("[2]",data)
		# data = client.run_cmd('cd /home/cssc/Documents/workspace && nohup geth --http --http.corsdomain="*" --http.api web3,eth,debug,personal,net,txpool,admin --http.addr=0.0.0.0 --vmdebug --datadir devnode  --allow-insecure-unlock --nodiscover > log 2>&1 &')['res']
		data = client.run_cmd("cd /home/cssc/Documents/workspace && chmod +x run.sh && ./run.sh")
		print("[3]", data)
		# 关闭连接
		client.close()
		# 记录下已处理
		recodes.append(ip)

	time.sleep(10)
	if len(tempIpdata) < 2 :
		continue
	# 开始按照拓扑建立连接
	for idx, ip in enumerate(tempIpdata):
		# 已经处理的跳过
		if ip in toporecodes:
			continue
		w3s = Web3(Web3.HTTPProvider('http://' + tempIpdata[idx] + ':8545'))
		if idx < 9:
			for tgtidx, v in enumerate(init_adjmatrix[idx]):
				# 建立连接
				if v == 1:
					w3t = Web3(Web3.HTTPProvider('http://' + tempIpdata[tgtidx] + ':8545'))
					# 得到node信息数据
					target_info = w3t.geth.admin.nodeInfo()
					target_peer = target_info["enode"].replace("127.0.0.1", tempIpdata[tgtidx])
					print("target_peer: ",target_peer)
					w3s.geth.admin.add_peer(target_peer)	
		# 处理后续加入的节点
		else:
			target_nodes = [ 
				[6, 7],
				[5, 8]
			]
			for idx in target_nodes[ random.choice(range(2)) ]:
				w3t = Web3(Web3.HTTPProvider('http://' + tempIpdata[idx] + ':8545'))
				# 得到node信息数据
				target_info = w3t.geth.admin.nodeInfo()
				target_peer = target_info["enode"].replace("127.0.0.1", tempIpdata[tgtidx])
				w3s.geth.admin.add_peer(target_peer)

		# 记录下已处理
		toporecodes.append(ip)
		print("[4] ", toporecodes)
