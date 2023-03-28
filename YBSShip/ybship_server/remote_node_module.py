import copy


class RNode(object):
    rnode_count = 0

    def __init__(self, ssh_info, node_name, node_folder_path, sh_local_path, sh_remote_path, httpweb3):
        RNode.rnode_count += 1
        self.ssh_info = copy.deepcopy(ssh_info)
        self.node_name = node_name
        self.node_folder_path = node_folder_path
        self.sh_local_path = sh_local_path
        self.sh_remote_path = sh_remote_path
        self.web3http = httpweb3

    def print(self):
        print(self.ssh_info, self.node_name, self.node_folder_path, self.sh_local_path, self.sh_remote_path, self.web3http)


