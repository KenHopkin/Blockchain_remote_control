# -*- coding: utf-8 -*-
from web3 import Web3
with open("./ipdata.txt", "r") as f:
	top_ip_7 = f.readlines()[:7]
	f.close()

print(top_ip_7)

changchuan = "enode://d90050e1be75feb7d8584c905f650a8405ba806f89d74d456300b12d3cfe895e0aacbe83671abbd2ffc69ccd275ba76e410a6e5a620c3e6945e6ff6110e057d3@192.168.10.226:30303?discport=0"

for ip in top_ip_7:
	print("{} is being handling...".format(ip))
	# 启动/重启geth
	w3t = Web3(Web3.HTTPProvider('http://' +ip[:-1] + ':8545'))
	# 得到node信息数据

	target_peer = changchuan
	w3t.geth.admin.add_peer(target_peer)

print("All of ip is finished.")
