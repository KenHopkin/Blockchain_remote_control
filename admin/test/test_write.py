

import copy
import json

from web3 import Web3
import datetime

import argparse
import os

if __name__ == "__main__":
    ass_grp = "thefirsttest"
    start_dev = 17
    end_dev = 26  # included
    time_add_device1 = datetime.datetime.now()
    time_add_device2 = datetime.datetime.now()

    result_str = "add device number " + str(end_dev-start_dev+1) + ", cost time:" \
                 + str(time_add_device2 - time_add_device1) + "秒 \n" + "each is " \
                 + str((time_add_device2 - time_add_device1)/(end_dev-start_dev+1)) + "\n"
    print(result_str[0], "__\n")
    print(result_str[1], "__\n")

    # print("add device number ", end_dev-start_dev+1, ", cost time:", (time_add_device2 - time_add_device1), "秒")
    with open("experiment_register.txt", 'a+') as register_result:
        register_result.write(result_str)
