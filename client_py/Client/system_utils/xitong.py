#!/usr/bin/env python
# coding:utf-8
import os
from log import gen_log
import platform
import sys
import subprocess
import shlex
import fileinput
import yingyong
# from subprocess import Popen
PWD = os.path.abspath(os.path.dirname(__file__))
os_dist = platform.dist()[0]
os_ver = platform.dist()[1].split('.')[0]


# 修改文件(文件完整路径,被替换的字符串，要替换的字符串)
def edit_file(filename, str1, str2):
    file_object = open(filename, 'rb')
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()

    new_text = all_the_text.replace(str1, str2)

    file_object = open(filename, 'wb')
    file_object.write(new_text)
    file_object.close()


# 追加内容
def add_str_to_file_end(filename, strs):
    file_object = open(filename, 'a')
    file_object.write(strs)
    file_object.close()

def insert_file(file_path, text, add_text):
    for line in fileinput.FileInput(file_path,inplace=1):
        if text in line:
            line = ''.join([line,add_text, '\r\n']).replace("\r", "")
        print line,

def dis_selinux():
    subprocess.call("setenforce" + " 0", shell=True)
    if os.path.exists('/etc/selinux/config'):
        edit_file('/etc/selinux/config', "SELINUX=enforcing", "SELINUX=disabled")


def set_dns():
    add_str_to_file_end('/etc/resolv.conf', 'nameserver 119.29.29.29')

def uninstall():  # 检查并卸载已安装的服务
    if os_dist == 'centos':
        cha = subprocess.Popen("rpm -qa | grep mysql", stdout=subprocess.PIPE, shell=True)
        output1 = cha.communicate()[0]
        print output1
        if output1.strip() == '':
            print 'none mysql'
        else:
            a = raw_input("注意看--------请输入Y确认卸载数据库！！！！！！！！！！！！:\n"*20)
            if a == 'Y':
                subprocess.call(['yum', 'erase', '-y', '*mysql-*'])
                print 'removed mysql'
            else :
                exit()
        chb = subprocess.Popen("rpm -qa | grep jdk", stdout=subprocess.PIPE, shell=True)
        output2 = chb.communicate()[0]
        print output2
        gen_log.info('where  jdk: %s',
                     output2)
        if output2.strip() == '':
            print 'none jdk'
        else:
            a = raw_input("注意看--------请输入Y确认卸载JDK！！！！！！！！！！！！:\n"*20)
	    if a == 'Y':
                subprocess.call(['yum', 'remove', '-y', '*jdk*'])
                gen_log.info('remove jdk')
            else:
                exit()
    elif os_dist == 'Ubuntu':
        dse = subprocess.Popen("aptitude search '~i|~M' -F '%p' | grep mysql",stdout=subprocess.PIPE,shell=True)
        output3 = dse.communicate()[0]
        if output3.strip() == '':
            print 'none mysql'
        else:
            a = raw_input("注意看--------请输入Y确认卸载数据库！！！！！！！！！！！！:\n"*20)
            if a == 'Y':
                subprocess.call(['apt-get', 'purge', '-y', 'mysql*.*'])
            else:
	        exit()
        dsj = subprocess.Popen("aptitude search '~i|~M' -F '%p' | grep jdk",stdout=subprocess.PIPE,shell=True)
        output4 = dsj.communicate()[0]	
        if output4.strip() == '':
            print 'none jdk'
        else:
            a = raw_input("注意看--------请输入Y确认卸载JDK！！！！！！！！！！！！:\n"*20)
            if a == 'Y':
                subprocess.call(['apt-get', 'purge', '-y', 'jdk*.*'])
            else:
	        exit()

def set_rpm():
    
    subprocess.call('yum --enablerepo=base --disablerepo=local* -y install yum-utils',shell=True)
    subprocess.call('yum-config-manager --disable local* *media', shell=True)
    subprocess.call('yum-config-manager --enable base updates extras updates ol6*', shell=True)
    subprocess.call('yum makecache -y fast', shell=True)
    subprocess.call('yum update -y', shell=True)
    subprocess.call('yum install -y ntp', shell=True)
    subprocess.call('service ntpd start', shell=True)
    subprocess.call('yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm', shell=True)
    subprocess.call('yum install python-setuptools', shell=True)
    subprocess.call('easy_install pip', shell=True)
    subprocess.call('mkdir -p ~/.pip/', shell=True)
    os.chdir("/root/.pip/")
    os.chdir("/root/")
    os.system('echo ~/.pip/pip.conf')
    
    add_str_to_file_end('/root/.pip/pip.conf', '''[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple''')
    
    subprocess.call('pip install requests', shell=True)
    subprocess.call('pip install wget', shell=True)
    subprocess.call(['yum',
 'install',
 '-y',
 'autoconf',
 'automake',
 'binutils',
 'bison',
 'flex',
 'gcc',
 'gcc-c++',
 'gettext',
 'libtool',
 'make',
 'patch',
 'pkgconfig',
 'rpm-build',
 'yum-utils',
 'yum-plugin-fastestmirror',
 'yum-plugin-downloadonly',
 'epel-release',
 'openssl-devel',
 'nc',
 'curl',
 'wget',
 'man',
 'nss',
 'vim',
 'system-config-network-tui',
 'bind-utils',
 'lokkit',
 'pciutils',
 'redhat-lsb-core',
 'libX11',
 'libXp',
 'telnet'])
    subprocess.call(['yum', 'groupinstall', '-y', 'chinese-support'])
    subprocess.call(['yum','install','-y','https://dev.mysql.com/get/mysql57-community-release-el6-9.noarch.rpm'])
    subprocess.call(['yum-config-manager', '--disable', 'mysql57-community'])
    subprocess.call(['yum-config-manager', '--enable', 'mysql56-community'])
    
    subprocess.call(['yum',
 'install',
 '-y',
 'mysql-community-server',
 'mysql-community-devel',
 'mysql-community-client'
 'mysql-community-libs-compat'])
    subprocess.call(['service', 'mysqld', 'start'])
    sql_list = ["DELETE FROM mysql.user WHERE User=\'\';",  
                "DELETE FROM mysql.user WHERE User=\'root\' AND Host NOT IN (\'localhost\', \'127.0.0.1\', \'::1\');",
                "DROP DATABASE test;",
                "FLUSH PRIVILEGES;"
                ]
    for sql in sql_list:
        sql = 'mysql -uroot -e "%s"' % sql
        os.system(sql)
    insert_file('/etc/my.cnf', '[mysqld]', 'character_set_server=utf8')
    subprocess.call(['service', 'mysqld', 'restart'])
    print "请改数据库密码:"

def apt_up():
    subprocess.call('apt-get update', shell=True)
    subprocess.call('apt-get upgrade', shell=True)
    subprocess.call('apt-get -y install build-essential libssl-dev libcurl4-openssl-dev unzip makepasswd lrzsz ntp language-pack-zh-hans-base python-pip python-dev libxp6', shell=True)
    subprocess.call('mkdir -p ~/.pip/', shell=True)
    os.chdir("/root/.pip/")
    os.chdir("/root/")
    os.system('echo ~/.pip/pip.conf')
    add_str_to_file_end('/root/.pip/pip.conf', '''[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple''')
    subprocess.call('pip install requests', shell=True)
    subprocess.call('pip install wget', shell=True)
    p1 = subprocess.Popen("debconf-set-selections", shell=True, stdin=subprocess.PIPE)
    p1.communicate("mysql-server mysql-server/root_password password pssesa")
    p2 = subprocess.Popen("debconf-set-selections", shell=True, stdin=subprocess.PIPE)
    p2.communicate("mysql-server mysql-server/root_password_again password pssesa")
    subprocess.call('apt-get install -y mysql-server-5.6 mysql-client-5.6 libmysqlclient-dev', shell=True)
    subprocess.call(['service', 'mysql', 'start'])
    sql_list = ["DELETE FROM mysql.user WHERE User=\'\';",
                "DELETE FROM mysql.user WHERE User=\'root\' AND Host NOT IN (\'localhost\', \'127.0.0.1\', \'::1\');",
                "DROP DATABASE test;",
                "FLUSH PRIVILEGES;"
                ]
    for sql in sql_list:
        sql = 'mysql -uroot -ppssesa -e "%s"' % sql
        os.system(sql)
    insert_file('/etc/mysql/my.cnf', '[mysqld]', 'character_set_server=utf8')
    insert_file('/etc/mysql/my.cnf', '[mysqld]', 'binlog_format=row')
    subprocess.call(['service', 'mysql', 'restart'])
                    
                    
#commands.getoutput('echo mysql-server mysql-server/root_password password pssesa | debconf-set-selections&&echo mysql-server mysql-server/root_password_again password pssesa | debconf-set-selections&&sudo apt-get -y install mysql-server-5.6 ')
'''
rl = requests.get('http://www.163.com')
data = rl.text

# 利用正则查找所有连接
link_list =re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" ,data)
for url in link_list:
    print url
'''
                    
def cxitong():
    if 10 in os.getgroups():  # centos sudo group is 10
        pass
    elif os.getuid() == 0:
        print 'root'
        subprocess.call("adduser axinfu", shell=True)
        subprocess.call("usermod -aG wheel axinfu", shell=True)
    else:
        sys.exit('no priv')  # panduan user is sudoer
    #dis_selinux()
    set_dns()

    # 检查并卸载已安装的服务
    uninstall()

    set_rpm()
    yingyong.set_jdk()
    yingyong.tomcat_set()
    yingyong.mysql_back()
    yingyong.redis_set()

def uxitong():
    if os.getuid() != 0:
        sys.exit('no root')
    set_dns()
    uninstall()
    apt_up()
    yingyong.set_jdk()
    yingyong.tomcat_set()
    yingyong.mysql_back()
    yingyong.redis_set()


