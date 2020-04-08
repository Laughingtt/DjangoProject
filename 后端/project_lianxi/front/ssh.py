SSHClient()的使用代码:
import paramiko

ssh = paramiko.SSHClient()  # 创建SSH对象
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='10.0.100.1', port=22, username='root', password='123456')
stdin, stdout, stderr = ssh.exec_command('ls')  # 执行命令
result = stdout.read()  # 获取命令结果
print(str(result, encoding='utf-8'))
ssh.close()  # 关闭连接

import paramiko

tran = paramiko.Transport(('xx.xx.xx.xx', 22))
tran.connect(username="root", password='xxx')
sftp = paramiko.SFTPClient.from_transport(tran)
localpath = "./your_name_szj.log"
remotepath = "/root/platform/your_name.log"
sftp.get(remotepath, localpath)
tran.close()

import paramiko

hostname = "10.0.100.1"
port = 22
username = "root"
password = "root"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password, compress=True)
channel = client.invoke_shell()  # 在SSH server端创建一个交互式的shell
command = ""
channel.send(command + '\n')
time.sleep(1)
stdout = channel.recv(1024 * 100000)
out_list = stdout.decode('utf-8').split("\n")
client.close()


#类方法实现
import platform
import subprocess
import paramiko
import time

class Ssh():

    def __init__(self):
        self.conn = None
        self.channel = None
        self.encoding = 'utf-8'

    def enc(self, msg):
        return bytes(msg, encoding=self.encording)

    def dec(self,byte):
        return str(byte, encoding=self.encording)

    def ping_server(self):
        host=platform.system()
        if find("Linux") >=0:
            res=subprocess.getoutput('ping %s'%ip)
        elif find("Windos") >=0:
            res = subprocess.getoutput('ping %s' % ip)
        else:
            res = -1
        return res

    def connect(self,hostname,port,username,password):
        self.conn = client = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.ping_server() != -1:
            self.conn.connect(hostname, port, username, password, compress=True)
            self.channel= self.conn.invoke_shell()

    def close(self):
        self.channel.send('exit\n')
        self.conn.close()

    def send(self,cmd):
        self.channel.send(self.enc(cmd))
        self.channel.send(self.enc("\n"))
        time.sleep(1)
        res=self.recv()
        return res

    def recv(self):
        res=self.channel.recv(1024*1000)
        res=self.dec(res)
        return res

if __name__ == "__main__":
    ip,port,user,passwd="","","",""
    ssh=Ssh()
    ssh.connect(ip,port,user,passwd)
    ssh.send(cmd)
    ssh.close()