import paramiko
# 远程登陆操作系统
def remoteSsh(sys_ip, username, command, password=''):
    try:
        # 创建ssh客户端
        client = paramiko.SSHClient()
        # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if len(password) == 0:
            print('互信方式远程连接')
            key_file = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
            client.connect(sys_ip, 22, username=username, pkey=key_file, timeout=20)
        else:
            print('密码方式远程连接') # base64.b64decode(password).decode()
            client.connect(sys_ip, 22, username=username, password=password, timeout=20)
        print(f"开始在远程服务器上执行指令:{command}")
        # 执行查询命令
        stdin, stdout, stderr = client.exec_command(f"""{command}""", get_pty=True)
        # 获取查询命令执c行结果,返回的数据是一个list
        result = stdout.read().decode('utf-8')
        print(f"{sys_ip}执行结果:", result)

        error = stderr.read().decode('utf-8')
        if error != "":
            print(f"{sys_ip}错误信息:", error)
        else:
            pass
    except Exception as e:
        print(e)
    finally:
        client.close()

# 批量执行同一命令
def batchExecuteRemoteCommand(host_list, command):
    import threading
    thread_list = []
    for ip, username, password in host_list:
        thread = threading.Thread(target = remoteSsh, args = (ip,username,password,command))
        thread_list.append(thread)#将生成的线程添加到列表里
    for t in thread_list:
        t.start() #开始执行线程
    for t in thread_list:
        t.join() #挂起线程，到所有线程结束



if __name__ == '__main__':
    local_server_ip = "192.168.102.37"
    local_server_username = "cssc"
    local_server_password = "cssc123"
    test_command = "ifconfig"
    remoteSsh(local_server_ip,local_server_username,test_command,local_server_password)

    local_server_ip = "192.168.102.44"
    local_server_username = "krace"
    local_server_password = "sklois123"
    test_command = "ifconfig"
    remoteSsh(local_server_ip, local_server_username, test_command, local_server_password)

