"""
@file: paramiko_test.py
@time: 2019/12/19
@author: alfons
"""
import paramiko

# 建立一个sshclient对象
with paramiko.SSHClient() as ssh:
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 调用connect方法连接服务器
    ssh.connect(hostname='10.10.160.30', port=22, username='root', password='cljslrl0620')

    # 执行命令
    # stdin, stdout, stderr = ssh.exec_command('ping 172.16.129.31 -c 4')
    stdin, stdout, stderr = ssh.exec_command('''ssh -o StrictHostKeyChecking=no sendoh@172.16.128.31 -p 22 
                                                "systemctl status linstor-satellite.service | grep -i 'Active: active (running)'"''')

    # 结果放到stdout中，如果有错误将放到stderr中
    print("stdout -> %s" % stdout.read().decode())
    print("stderr -> %s" % stderr.read().decode())

    # with ssh.open_sftp() as sftp:
    #     f = sftp.open("/tmp/summary.log")
    #     sftp.rename("/tmp/summary.log", "/tmp/sum.log.bak")
    #     pass
    ssh.close()