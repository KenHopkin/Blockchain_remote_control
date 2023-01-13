import os
import argparse

parser= argparse. ArgumentParser()
parser.add_argument("-json", type=str, help="the name of blockchain config json ", default='gen_zczs.json')
args= parser.parse_args()

init_command = 'geth --datadir ./adminnode init ' + args.json

res1 = os.popen(init_command).readlines()

res2 = os.popen('geth --http --http.corsdomain="*" --http.api web3,eth,debug,personal,net,txpool,admin --http.addr=0.0.0.0 --vmdebug --datadir  ./adminnode/ --allow-insecure-unlock --nodiscover 1>>adminnode.log').readlines()

