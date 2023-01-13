from time import sleep 
from socket import *

def get_host_ip():
    try:
        s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s1.connect(('8.8.8.8', 80))
        ip = s1.getsockname()[0]
    finally:
        s1.close()

    return ip

if __name__ == '__main__':

    # print(get_host_ip())
    dest = ('255.255.255.255', 1520)
    ip = get_host_ip()
    data = ip

    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST,1)

    while True:
       sleep(2)
       s.sendto(data.encode(),dest)
    s.close()
