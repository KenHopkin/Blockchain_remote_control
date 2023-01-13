from web3 import Web3
import cert_module as cert_module
import time
import random


class Node(object):
    """
    每个无人艇都可视为一个Node
    """
    node_count = 0
    addr_weight_lst = []
    nodes_addr = []

    def __init__(self, w3, contract, identity, addr):
        self.w3 = w3
        self.contract = contract
        self.id = identity
        self.addr = addr
        self.node_idx = 0
        self.cert = []
        self.domain_admin = []
        self.domain_ass = []
        # self.domain_id = ""

        self.computing = random.randint(0, 100)
        self.battery = random.randint(0, 100)
        self.communication = random.randint(0, 100)
        self.lgt = str(random.uniform(114, 118))
        self.ltt = str(random.uniform(12, 16))
        self.idx = 0
        self.wgt = self.computing + self.battery + self.communication
        self.last_heartbeat = 0
        self.response_frequency = 0.00
        Node.node_count += 1
        Node.nodes_addr.append(self.addr)

    def mas_create_other_cert(self, other, domain_id):
        cert_hash = Web3.toHex(self.contract.functions.GetCertHash(domain_id, other.id, other.addr).call())
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        cert_sig = Web3.toHex(self.w3.eth.sign(self.addr, hexstr=cert_hash))
        other.cert.append(cert_module.Cert(self.addr, domain_id, other.id, other.addr, cert_sig))

    def mas_rst_contract(self, indexnode):
        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[indexnode], "123456")
        tx_hash = self.contract.functions.ResetAll().transact({'from': self.w3.eth.accounts[indexnode]})
        # self.w3.geth.miner.start(4)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

    def mas_rst_contract2(self, masteraddr):
        self.w3.geth.personal.unlock_account(masteraddr, "123456")
        tx_hash = self.contract.functions.ResetAll().transact({'from': masteraddr})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

    def mas_build_domain(self, master_id, domain_id):
        """
        用于创建信任域
        :param domain_id: 输入信任域的ID（字符串）
        :return: 字符串，信任域的创建结果
        """
        len_domain = self.contract.functions.LenMasterDomain(self.addr).call()
        if len_domain == 0:
            before = True
        else:
            before = False if self.contract.functions.MasterDomain(self.addr, len_domain - 1).call() == domain_id \
                else True

        # 获取master的创建信任域请求的签名
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        build_sig = \
            Web3.toHex(self.w3.eth.sign(self.addr, self.contract.functions.GetBuildHash(self.addr, domain_id).call()))
        print("hash:", Web3.toHex(self.contract.functions.GetBuildHash(self.addr, domain_id).call()))
        print("domain_id:", domain_id)
        print("master addr:", self.addr)
        print("build_sig:", build_sig)
        print("typeof build_sig", type(build_sig))
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        tx_hash = self.contract.functions.BuildPhase(self.addr, master_id, domain_id, build_sig) \
            .transact({'from': self.addr})
        # self.w3.geth.miner.start(2)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

        len_domain = self.contract.functions.LenMasterDomain(self.addr).call()
        after = True if self.contract.functions.MasterDomain(self.addr, len_domain - 1).call() == domain_id else False

        if before & after:
            self.domain_admin.append(domain_id)
            self.update_heartbeat()
            self.election(domain_id)
            self.broadcast(domain_id)
            return "py: the building of domain is successful"
        else:
            try:
                raise ValueError("py: the building of domain is failure.", "before=", before, "after=", after)
            except ValueError:
                raise

    def fault_build_domain(self, master_id, fault_addr, domain_id):
        """
        用于创建信任域
        :param domain_id: 输入信任域的ID（字符串）
        :return: 字符串，信任域的创建结果
        """
        len_domain = self.contract.functions.LenMasterDomain(self.addr).call()
        if len_domain == 0:
            before = True
        else:
            before = False if self.contract.functions.MasterDomain(self.addr, len_domain - 1).call() == domain_id \
                else True

        # 获取master的创建信任域请求的签名
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        build_sig = \
            Web3.toHex(self.w3.eth.sign(self.addr, self.contract.functions.GetBuildHash(self.addr, domain_id).call()))
        print("hash:", Web3.toHex(self.contract.functions.GetBuildHash(self.addr, domain_id).call()))
        print("domain_id:", domain_id)
        print("master addr:", self.addr)
        print("build_sig:", build_sig)
        print("typeof build_sig", type(build_sig))
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        if(fault_addr != self.addr):
            try:
                raise ValueError("The Master Signature of Building Request is invalid.\n")
            except ValueError:
                tx_hash = self.contract.functions.BuildPhase(fault_addr, master_id, domain_id, build_sig) \
                    .transact({'from': self.addr})
                raise
        tx_hash = self.contract.functions.BuildPhase(fault_addr, master_id, domain_id, build_sig) \
            .transact({'from': self.addr})
        # self.w3.geth.miner.start(2)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

        len_domain = self.contract.functions.LenMasterDomain(self.addr).call()
        after = True if self.contract.functions.MasterDomain(self.addr, len_domain - 1).call() == domain_id else False

        if before & after:
            self.domain_admin.append(domain_id)
            self.update_heartbeat()
            self.election(domain_id)
            self.broadcast(domain_id)
            return "py: the building of domain is successful"
        else:
            try:
                raise ValueError("py: the building of domain is failure.", "before=", before, "after=", after)
            except ValueError:
                raise

    def device_association(self, index, nodeindex):
        """
        该无人艇利用已经存储的证书来加入相应的信任域
        :param index: 表示用自身存储的第 index 个证书来加入证书上相应的信任域
        :return:
        """

        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[nodeindex], "123456")
        device_sig = Web3.toHex(
            self.w3.eth.sign(self.w3.eth.accounts[nodeindex], self.contract.functions.GetAssociationHash(
                self.cert[index].domain_id, self.cert[index].device_id, self.cert[index].device_addr,
                self.cert[index].sig).call()))

        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[nodeindex], "123456")

        tx_hash = self.contract.functions.AssociationPhase(self.cert[index].domain_id, self.cert[index].device_id,
                                                           self.cert[index].device_addr, self.cert[index].sig,
                                                           device_sig) \
            .transact({'from': self.w3.eth.accounts[nodeindex]})
        # self.w3.geth.miner.start(2)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

        res_used, res_id, res_addr, _, _, _ = self.contract.functions.ViewDeviceByID(self.cert[index].domain_id,
                                                                                     self.cert[index].device_id).call()
        if res_used and res_id == self.cert[index].device_id and res_addr == self.cert[index].device_addr:
            self.domain_ass.append(self.cert[index].domain_id)
            self.update_heartbeat()
            return "the device:" + res_id + " at " + res_addr + " is associated successfully!"
        else:
            try:
                raise ValueError("the device:", res_id, "at", res_addr, "is associated failure!")
            except ValueError:
                raise

    def device_resign(self, index, nodeindex):
        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[nodeindex], "123456")
        device_sig = Web3.toHex(
            self.w3.eth.sign(self.w3.eth.accounts[nodeindex], self.contract.functions.GetAssociationHash(
                self.cert[index].domain_id, self.cert[index].device_id, self.cert[index].device_addr,
                self.cert[index].sig).call()))

        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[nodeindex], "123456")

        tx_hash = self.contract.functions.DetouchPhase(self.cert[index].domain_id, self.cert[index].device_id,
                                                           self.cert[index].device_addr, self.cert[index].sig,
                                                           device_sig) \
            .transact({'from': self.w3.eth.accounts[nodeindex]})
        # self.w3.geth.miner.start(2)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

        res_used, res_id, res_addr, _, _, _ = self.contract.functions.ViewDeviceByID(self.cert[index].domain_id,
                                                                                     self.cert[index].device_id).call()
        if not (res_used and res_id == self.cert[index].device_id and res_addr == self.cert[index].device_addr):
            # self.domain_ass.append(self.cert[index].domain_id)
            # self.update_heartbeat()
            return "the device:" + res_id + " at " + res_addr + " is resigned successfully!"
        else:
            try:
                raise ValueError("the device:", res_id, "at", res_addr, "is resigned failure!")
            except ValueError:
                raise

    def device_au(self, nodeindex, domain_id, device_id, device_data):
        """
        在自身已加入的信任域（domain_id）内，对无人艇（device_id）发送数据（device_data）
        :param domain_id: 信任域的ID
        :param device_id: 无人艇的ID
        :param device_data: 需要发送的数据
        :return:
        """
        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[nodeindex], "123456")
        device_sig = Web3.toHex(
            self.w3.eth.sign(self.w3.eth.accounts[nodeindex], self.contract.functions.GetAthenticationHash(
                domain_id, device_id, device_data).call()))

        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[nodeindex], "123456")
        tx_hash = self.contract.functions.AthenticationPhase(domain_id, device_id, device_data, device_sig) \
            .transact({'from': self.w3.eth.accounts[nodeindex]})
        # self.w3.geth.miner.start(2)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

        lst_len = self.contract.functions.LenDomainInfoDeviceData(domain_id, device_id).call()
        recorded = self.contract.functions.ViewData(domain_id, device_id, lst_len - 1).call()
        # print("recorded:", recorded)
        # print(type(recorded))
        if device_data == recorded[0]:
            return "py: The authentication is successful, the device data has been sent, and the data is that \"" \
                   + device_data + "\""
        else:
            try:
                raise ValueError("py: the authentication is failure.", "device_data=", device_data, "recorded=",
                                 recorded)
            except ValueError:
                raise

    def mas_manage(self, accountindex, domain_id, device_id, flag):
        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[accountindex], "123456")
        mas_sig = Web3.toHex(self.w3.eth.sign(self.w3.eth.accounts[accountindex], self.contract.functions.GetManageHash(
            self.addr, domain_id, device_id, flag).call()))

        self.w3.geth.personal.unlock_account(self.w3.eth.accounts[accountindex], "123456")
        tx_hash = self.contract.functions.ManagementPhase(self.addr, domain_id, device_id, flag, mas_sig) \
            .transact({'from': self.w3.eth.accounts[accountindex]})
        # self.w3.geth.miner.start(2)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()

        _, res_id, _, permission, _, _ = self.contract.functions.ViewDeviceByID(domain_id, device_id).call()

        if res_id == device_id and permission == flag:
            return "py: The management is successful, the device\'s permission has been changed to ", flag
        else:
            try:
                raise ValueError("py: the management is failure.", "res_id=", res_id, "permission=", permission)
            except ValueError:
                raise

    # dynamic election related



    def mine_current_transact(self, tx_hash):
        # self.w3.geth.miner.start(4)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        # self.w3.geth.miner.stop()
        return tx_receipt

    def distribute(self):

        for i in range(len(Node.nodes_addr)):
            if Node.nodes_addr == self.addr: continue
            # self.unlock_account(0, "123456")
            tx_hash = self.w3.eth.sendTransaction(
                {'to': Node.nodes_addr[i], 'from': self.addr, 'value': 1000000000000000000})
            self.mine_current_transact(tx_hash)
            print(i, ":", self.w3.eth.getBalance(Node.nodes_addr[i]))

    def update_heartbeat(self):
        # self.unlock_account(0, "123456")
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        tx_hash = self.contract.functions.update_heartbeat(self.computing, self.battery, self.communication, self.lgt, self.ltt) \
            .transact({'from': self.addr})
        self.mine_current_transact(tx_hash)
        print(self.id, "heartbeat time: {}".format(int(time.time())))

    # def inquiry_superior(self):
    #     superior = self.contract.functions.superior_addr().call()
    #     return superior

    def data_submission(self, data):
        # self.unlock_account(0, "123456")
        tx_hash = self.contract.functions.send_data(self.inquiry_superior(), data) \
            .transact({'from': self.addr})
        self.mine_current_transact(tx_hash)

    def respond_message(self):
        # self.unlock_account(0, "123456")
        tx_hash = self.contract.functions.respond_msg().transact({'from': self.addr})
        self.mine_current_transact(tx_hash)

    def init_node_self(self):
        # self.unlock_account(0, "123456")
        tx_hash = self.contract.functions.init_self(self.id).transact({'from': self.addr})
        self.mine_current_transact(tx_hash)

    def partition(self, arr, low, high):
        i = (low - 1)  # 最小元素索引
        pivot = arr[high][0]

        for j in range(low, high):

            # 当前元素小于或等于 pivot
            if arr[j][0] <= pivot:
                i = i + 1
                arr[i][0], arr[j][0] = arr[j][0], arr[i][0]
                arr[i][1], arr[j][1] = arr[j][1], arr[i][1]

        arr[i + 1][0], arr[high][0] = arr[high][0], arr[i + 1][0]
        arr[i + 1][1], arr[high][1] = arr[high][1], arr[i + 1][1]
        return (i + 1)

    # arr[] --> 排序数组
    # low  --> 起始索引
    # high  --> 结束索引

    # 快速排序函数
    def quicksort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)

            self.quicksort(arr, low, pi - 1)
            self.quicksort(arr, pi + 1, high)

    def sort_all_nodes(self, low, high):
        Node.addr_weight_lst.clear()
        i = self.contract.functions.nodes_iterate_start().call()
        while self.contract.functions.nodes_iterate_valid(i).call():
            wgt, addr = self.contract.functions.nodes_iterate_get_addr_wgt(i).call()
            Node.addr_weight_lst.append([wgt, Web3.toChecksumAddress(addr)])
            i = self.contract.functions.nodes_iterate_next(i).call()
        self.quicksort(Node.addr_weight_lst, low, high)
        print(Node.addr_weight_lst)

        wgt_list = [j[0] for j in Node.addr_weight_lst]
        addr_list = [j[1] for j in Node.addr_weight_lst]
        print(wgt_list, "\n", addr_list)
        return wgt_list, addr_list

    def init_network_solsort(self, domain_id):
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        tx_hash = self.contract.functions.init_phase_solsort(domain_id).transact({'from': self.addr})
        self.mine_current_transact(tx_hash)

    def print_weight_list(self):
        Node.addr_weight_lst.clear()
        len = self.contract.functions.query_weight_len().call()
        for i in range(len):
            addr, val = self.contract.functions.query_weight_byindex(i).call()
            print(addr, val)

    def show_weight(self):
        print(self.addr, self.computing, self.battery, self.communication, self.wgt)

    def re_random_weight(self):
        self.computing = random.randint(0, 100)
        self.battery = random.randint(0, 100)
        self.communication = random.randint(0, 100)
        self.wgt = self.computing + self.battery + self.communication
        self.show_weight()

    def query_weight(self, domain_id, dev_id):
        print(self.addr, self.contract.functions.query_lgtlttwh(domain_id, dev_id).call()[2])

    def check_ele_time(self):
        return self.contract.functions.check_election_time().call()

    def check_heartbeat(self, domain_id, device_id):
        return self.contract.functions.query_lgtlttwh(domain_id, device_id).call()[3]

    def query_lgtlttwh(self, domain_id, device_id):
        return self.contract.functions.query_lgtlttwh(domain_id, device_id).call()

    def query_lgtltt(self, domain_id, device_id):
        return self.contract.functions.query_lgtlttwh(domain_id, device_id).call()[0:2]

    def election(self, domain_id):
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        tx_hash = self.contract.functions.election_phase(domain_id).transact({'from': self.addr})
        self.mine_current_transact(tx_hash)

    def broadcast(self, domain_id):
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        tx_hash = self.contract.functions.leader_broadcast(domain_id).transact({'from': self.addr})
        self.mine_current_transact(tx_hash)

    def query_dm_leader(self, domain_id):
        leader_addr, _, _, _, _, _ = self.contract.functions.query_DN(domain_id).call()
        return leader_addr

    def query_dm_deputy_leader(self, domain_id):
        _, deputy_leader, _, _, _, _ = self.contract.functions.query_DN(domain_id).call()
        return deputy_leader

    def query_election_result(self, domain_id):
        _, _, result, _, _, _ = self.contract.functions.query_DN(domain_id).call()
        return result

    # iterate device's domain
    def dev_dm_iterate_start(self):
        return self.contract.functions.iterate_start(self.addr).call()

    def dev_dm_can_iterate(self, curr):
        return self.contract.functions.can_iterate(self.addr, curr).call()

    def dev_dm_iterate_next(self, curr):
        return self.contract.functions.iterate_next(self.addr, curr).call()

    def change_para(self, heartbeat_interval, election_interval, sent_responded_factor):
        self.w3.geth.personal.unlock_account(self.addr, "123456")
        tx_hash = self.contract.functions.upd_para(heartbeat_interval, election_interval, sent_responded_factor).transact({'from': self.addr})
        self.mine_current_transact(tx_hash)
