# encoding: utf-8
import socket
import re
import multiprocessing

def service_client(new_socket, ips):
    """为这个客户端返回数据"""
 
    # 1. 接收浏览器发送过来的请求 ，即http请求
    # GET / HTTP/1.1
    # print("service_client")
    # request = new_socket.recv(1024).decode("utf-8")
 
    # request_lines = request.splitlines()
    # print("")
    # print(">" * 20)
    # print(request_lines)
 
    # GET /index.html HTTP/1.1
    # get post put del
    # file_name = ""
    # print(request_lines[0])
    # request_lines = new_socket
    # ret = re.search(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", request_lines)
    ret = str(new_socket)
    if ret:
        # ip = ret.group(0)
        ip = ret
        # print(ip)
        # 去重
        if ip not in ips:
            ips.append(ip)
    # ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])  #获取请求文件名
    # if ret:
    #     file_name = ret.group(1)
    #     # print("*"*50, file_name)
    #     if file_name == "/":
    #         file_name = "/index.html"
 
    # 2. 返回http格式的数据，给浏览器
 
    # try:
    #     f = open("./html" + file_name, "rb")
    # except: #对于没有找到请求文件路径的返回结果
    #     response = "HTTP/1.1 404 NOT FOUND\r\n"
    #     response += "\r\n"
    #     response += "------file not found-----"
    #     new_socket.send(response.encode("utf-8"))
    # else:
    # html_content = f.read()
    # f.close()
    # 2.1 准备发送给浏览器的数据---header
    # response = "HTTP/1.1 200 OK\r\n"
    # response += "\r\n"
    # 2.2 准备发送给浏览器的数据---boy
    # response += "hahahhah"

    # 将response header发送给浏览器
    # new_socket.send(response.encode("utf-8"))
    # 将response body发送给浏览器
    # new_socket.send(html_content)

    # 关闭套接
    # new_socket.close()


def ReveiveIPs(ips):
    """用来完成整体的控制"""
    # 1. 创建套接字
    # tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    # 2. 绑定
    tcp_server_socket.bind(("", 1520))
    print("Listening for broadcast at ", tcp_server_socket.getsockname())
    # 3. 变为监听套接字
    # tcp_server_socket.listen(128)

    while True:
        # 4. 等待新客户端的链接
        # new_socket, client_addr = tcp_server_socket.accept()
        ip_data, client_addr = tcp_server_socket.recvfrom(65535)
        ip_data = bytes.decode(ip_data)
        # print("aaaaaaaaaaaaa",ip_data)
 
        # 5. 为这个客户端服务,这里启动多进程去处理服务器接收的请求
        p = multiprocessing.Process(target=service_client, args=(ip_data,ips,))
        p.start()  # 同样，子进程都是用start()方法启动
        # new_socket.close()  #注意使用多进程以后这里多了一个close().之前单进程没有的。主进程和子进程都要关闭。
 
    # 关闭监听套接字
    tcp_server_socket.close()
