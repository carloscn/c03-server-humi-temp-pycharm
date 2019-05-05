#coding=utf-8


import socket
import select
import SocketServer
from multiprocessing import Process
import os
import os.path
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')
rootdir = "./"
current_time = ""

# 创建一个类
class ChatServer:
    # 初始化 传入监听端口即可
    def __init__(self, port):
        self.port = port
        # 配置参数
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind(("", port))
        self.srvsock.listen(10)  # 设置监听数量
        # 添加在线服务器
        self.descripors = [self.srvsock]
        print("Server started!")

    # 运行监听方法
    def run(self):
        while True:
            # 获取 新的连接申请
            (sread, swrite, sexc) = select.select(self.descripors, [], [])
            # 读 以获取到的申请
            for sock in sread:
                # 判断是否有新的连接
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    # 读接收到的消息
                    str_send = sock.recv(1024).decode('gbk')  # 读缓冲区大小1024
                    # 检测是否断开连接
                    host, port = sock.getpeername()
                    if str_send == '':
                        str_send = 'Client left %s:%s\r\n' % (host, port)
                        self.broadcast_str(str_send, sock)
                        sock.close
                        self.descripors.remove(sock)
                    else:
                        newstr = '[%s:%s] %s' % (host, port, str_send)
                        self.broadcast_str(newstr, sock)

    # 建立一个新的连接客户机
    def accept_new_connection(self):
        # 接收请求
        newsock, (remhost, remport) = self.srvsock.accept()
        # 添加连接
        self.descripors.append(newsock)
        newsock.send("You are Connected\r\n".encode('utf8'))
        str_send = 'Client joined %s:%s' % (remhost, remport)
        self.broadcast_str(str_send, newsock)

    # 广播函数
    def broadcast_str(self, str_send, my_sock):
        # 遍历已有连接
        for sock in self.descripors:
            if sock != self.srvsock and sock != my_sock:
                sock.send(str_send.encode('utf8'))
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        current_time = current_time + "#"
        if str_send.__contains__("#"):
            str_s = str_send.split("#")
            saveStr = current_time + "温度: " + str_s[1] + " 湿度: " + str_s[2] + "\n"
            fileHandle =     open("mem.txt", 'a')
            fileHandle.write(saveStr)
            fileHandle.close()
        print("转发内容:" + current_time + str_send + "  --- send ok!")


if __name__ == '__main__':
    ChatServer(5555).run()