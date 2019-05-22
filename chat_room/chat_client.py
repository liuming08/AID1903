

from socket import *
import os,sys

# 服务器地址
ADDR = ("176.215.155.172",8888)

# 发送消息
def send_msg(s,name):
    while True:
        try:
            text = input("说:")
        except KeyboardInterrupt:
            text = "quit"
        # 退出聊天室
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

# 接收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        # 服务端发送EXIT表示客户端退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode()+"\n发言:",end="")


# 创建网络连接
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        # 等待回应
        data,addr = s.recvfrom(1024)
        if data.decode() == "OJBK":
            print("敌军还有5秒到达战场")
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s)


if __name__ == "__main__":
    main()