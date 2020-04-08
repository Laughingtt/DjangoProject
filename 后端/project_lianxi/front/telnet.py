import logging
import telnetlib
import time


class TelnetClient():
    def __init__(self, ):
        self.tn = telnetlib.Telnet()

    # 此函数实现telnet登录主机
    def login_host(self, host_ip, username, password):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip, port=23)
        except:
            logging.warning('%s网络连接失败' % host_ip)
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'login: ', timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password: ', timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logging.warning('%s登录成功' % host_ip)
            return True
        else:
            logging.warning('%s登录失败，用户名或密码错误' % host_ip)
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self, command):
        # 执行命令
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        # 获取命令结果
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.warning('命令执行结果：\n%s' % command_result)

    # 退出telnet
    def logout_host(self):
        self.tn.write(b"exit\n")


if __name__ == '__main__':
    host_ip = '192.168.220.129'
    username = 'root'
    password = 'abcd1234'
    command = 'whoami'
    telnet_client = TelnetClient()
    # 如果登录结果返加True，则执行命令，然后退出
    if telnet_client.login_host(host_ip, username, password):
        telnet_client.execute_some_command(command)
        telnet_client.logout_host()

import platform
import subprocess
import telnetlib
import time

class Telnet():

    def __init__(self):
        self.conn = None
        self.encoding = 'utf-8'

    def enc(self, msg):
        return bytes(msg, encoding=self.encording)

    def dec(self,byte):
        return str(byte, encoding=self.encording)

    def ping_server(self):
        host=platform.system()
        if find("Linux") >0:
            res=subprocess.getoutput('ping %s'%ip)
        elif find("Windos") >0:
            res = subprocess.getoutput('ping %s' % ip)
        else:
            res = -1
        return res
    def connect(self,ip,port):
        self.ping_server()
        self.conn = telnetlib.Telnet(ip, port)
        self.login()

    def close(self):
        self.close()

    def send(self,cmd):
        self.conn.write(self.enc(cmd))
        self.conn.write(self.enc("\n"))
        time.sleep(1)
        res=self.recv()

    def recv(self):
        res=self.conn.read_very_eager()
        res=self.dec(res)
        return res

    def login(self,username,password):
        self.conn.read_until(b'login: ', timeout=10)
        self.conn.send(username)
        self.conn.read_until(b'Password: ', timeout=10)
        self.conn.send(password)
        return "succeed"

if __name__ == "__main__":
    ip,port,cmd="","".""
    telnet=Telnet()
    telnet.connect(ip,port)
    telnet.send(cmd)
    telnet.close()