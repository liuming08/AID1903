from socket import *
import sys
import time


# 具体功能
class FtpClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")  # 发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # OK表示请求成功
        if data == "OK":
            # 接收文件列表
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self, filename):
        # 发送请求
        self.sockfd.send(("G " + filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            fd = open(filename, "wb")
            # 接收内容,写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b"##":
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self, filename):
        try:
            f = open(filename, "rb")
        except Exception:
            print("没有该文件")
            return
        # 发送请求
        filename = filename.split("/")[-1]
        self.sockfd.send(("P " + filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b"##")
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)


# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)

    while True:
        print("\n==========命令选项==========")
        print("**********1.list************")
        print("********2.get file**********")
        print("********3.put file**********")
        print("**********4.quit************")
        print("============================")

        cmd = input("输入命令(1/2/3/4):")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put(filename)


# 网络连接
def main():
    # 服务器地址
    ADDR = ("127.0.0.1", 6731)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接服务器失败")
        print(e)
        return
    else:
        print("""
            ************************
            Data  File  Image  Video
             1     2      3      4
            ************************
        """)
        cls = input("请选择文件种类:")
        if cls not in ["Data", "File", "Image", "Video"]:
            print("Sorry Input Error")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)  # 发送具体请求


if __name__ == "__main__":
    main()
