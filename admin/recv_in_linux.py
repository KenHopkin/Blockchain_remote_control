# coding:utf-8
"""
本文件实现Linux的recv端，用于接收并解析windows发来的所有AIS信息，从中选择我们需要的经纬度并提取
"""
import socket

MESSAGE_EXAMPLE = "1014201##120.235481##9.931233####123789456##125.945831##36.445831####"

NODE_USER_NUM_LIST = []


class recvInLinux:
    def __init__(self, prefix, tcp_server_ip, tcp_server_port):
        self.prefix = prefix
        self.tcp_server_ip = tcp_server_ip
        self.tcp_server_port = tcp_server_port
        self.node_user_num = None
        self.longitude = None
        self.latitude = None

    def get_node_user_num(self):
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.connect((self.tcp_server_ip, self.tcp_server_port))
        data_from_server = tcp_client_socket.recv(1024).decode("utf-8")
        if data_from_server != "":
            print("Data From Windows Simulator: {}".format(data_from_server))
            data_groups = data_from_server.split("####")[:-1]
            for data_group in data_groups:
                node_user_num = data_group.split("##")[0]
                if node_user_num[:3] == self.prefix:
                    if node_user_num not in NODE_USER_NUM_LIST:
                        self.node_user_num = data_group.split("##")[0]
                        NODE_USER_NUM_LIST.append(self.node_user_num)
                        break
        tcp_client_socket.close()
        return self.node_user_num

    def analyze_id_longitude_latitude(self, data_string):
        data_groups = data_string.split("####")[:-1]
        for data_group in data_groups:
            if data_group.split("##")[0] == self.node_user_num:
                longitude = float(data_group.split("##")[1])  # 经度
                latitude = float(data_group.split("##")[2])  # 纬度
                break
        return longitude, latitude

    def get_node_longitude_latitude(self):
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.connect((self.tcp_server_ip, self.tcp_server_port))
        data_from_server = tcp_client_socket.recv(1024).decode("utf-8")
        if data_from_server != "":
            print("Data From Windows Simulator: {}".format(data_from_server))
            self.longitude, self.latitude = self.analyze_id_longitude_latitude(data_from_server)
        tcp_client_socket.close()
        return self.longitude, self.latitude

    def get_longtitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude


if __name__ == '__main__':

    node_user_num = "1014201"
    tcp_server_ip = "192.168.10.199"
    tcp_server_port = 50500
    r = recvInLinux(node_user_num, tcp_server_ip, tcp_server_port)

    print("longitude, latitude:", r.get_node_longitude_latitude())
    print("longitude:", r.get_longtitude())
    print("latitude:", r.get_latitude())
