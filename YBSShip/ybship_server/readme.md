# 项目节点启动和连接指引
## 自动启动节点

当能够网络连接进入项目部署的服务器所在的局域网中时，可以采取自动启动节点的方式。

### 源代码地址

HTTPS: `https://github.com/KenHopkin/Blockchain_remote_control.git`

SSH: `git@github.com:KenHopkin/Blockchain_remote_control.git`

GitHub CLI: `gh repo clone KenHopkin/Blockchain_remote_control`

### 前提条件

- 网络连接进入项目部署的服务器所在的局域网中。

- 要求各个虚拟机的ip地址没有变化，即地址为 `192.168.10.231~235`和`192.168.10.206~225`。

- 如果虚拟机的ip地址发生变化，则需要修改`YBSShip/ybship_server/xxw_batch_node_cssc_singleproc.py`中第131行-第136行的ip地址，以及`YBSShip/ybship_server/xxw_batch_node_cssc_singleproc_onlystart.py`中第131行-第136行的ip地址。


### 节点启动和互相连接

- 如果各个虚拟机的ip地址没有变化，则运行`YBSShip/ybship_server/xxw_batch_node_cssc_singleproc_onlystart.py`即可完成节点的启动和连接。
- 如果虚拟机的ip地址发生变化，则在按照前提条件修改了代码中的ip地址后，可以运行`YBSShip/ybship_server/xxw_batch_node_cssc_singleproc.py`，即可完成节点启动和连接

