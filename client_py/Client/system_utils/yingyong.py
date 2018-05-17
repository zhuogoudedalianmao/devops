#!/usr/bin/env python
# coding:utf-8
import shutil
import tarfile
import requests
import glob
import os
import shlex
import subprocess
import xitong
import config
import wget
import platform
import re
import wget
import sys
os_dist = platform.dist()[0]

'''
def __init__(self):
    jdk_gz_file_path = config.Config.JDK_GZ_PATH
    jdk_down_url = config.Config.JDK_URL
    redis_down_url = config.Config.REDIS_URL
'''

def download(url,desfile):
    with open(desfile,'wb') as code:
        r = requests.get(url,stream=True,timeout=3600)
        total_length = int(r.headers['Content-Length']) / 1024
        if total_length is None:
            code.write(r.content)
        else:
            dl = 0
            for data in r.iter_content(chunk_size=1024):
                dl += len(data)
                code.write(data)
                done = int((dl / total_length) / 20.48)
                sys.stdout.write("\r[%s%s]" % ('█' * done, done*2))
                sys.stdout.flush()
        print('下载完成：%s' %desfile)


def un_tar(file_name):
    """untar zip file"""
    tar = tarfile.open(file_name)
    names = tar.getnames()
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for name in names:
        tar.extract(name, file_name + "_files/")
    tar.close()

def set_jdk():
    download(config.Config.JDK_URL, config.Config.JDK_GZ_PATH)
    un_tar(config.Config.JDK_GZ_PATH)
    if not os.path.exists('/usr/lib/jvm'):
           subprocess.call('mkdir /usr/lib/jvm', shell=True)
    jdk_untar_dir = glob.glob(config.Config.JDK_GZ_PATH + "_files/j*")[0]
    os.system("mv /root/jdk.tar.gz_files/fonts/* /usr/share/fonts/")
    os.environ['JDK_UNTAR_DIR'] = jdk_untar_dir[:-11]
    shutil.move (jdk_untar_dir, '/usr/lib/jvm')
    subprocess.call(shlex.split('update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.7.0_80/bin/java" 1'))
    subprocess.call(shlex.split('update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.7.0_80/bin/javac" 1'))
    subprocess.call(shlex.split('update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/jdk1.7.0_80/bin/javaws" 1'))
    xitong.add_str_to_file_end('/etc/profile', """export JAVA_HOME=/usr/lib/jvm/jdk1.7.0_80
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
""")

def redis_set():
    print "download"
    download(config.Config.REDIS_URL, './redis-stable.tar.gz')
    un_tar('./redis-stable.tar.gz')
    redis_src_dir = glob.glob('./redis-stable.tar.gz_files/redis*')[0]
    os.chdir(redis_src_dir)
    subprocess.call('make', shell=True)
    subprocess.call('make install', shell=True)
    os.chdir( './utils')
    subprocess.call('./install_server.sh', shell=True)

def tomcat_set():
    #shutil.move("/root/tomcat.py",config.Config.TOMCAT_PATH)
    tomcat_url = config.Config.TOMCAT_URL
    r = requests.get(tomcat_url)
    data = r.text
    # 利用正则查找所有连接
    a = list()
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
    for url in link_list:
        a.append(url)
    url_version = a[-1]
    url_front = ''.join(
        [tomcat_url, url_version, 'bin/apache-tomcat-'])
    url_back = url_version[1:-1]
    os.environ['TOMCAT_VER'] = url_back
    url_all = ''.join([url_front, url_back, '.tar.gz'])
    dfile_name = wget.download(url_all)
    un_tar(dfile_name)
    tomcat_untar_dir = glob.glob(''.join([dfile_name, "_files/a*"]))[0]
    my_home = ''.join(['/home/', config.Config.user])
    shutil.move(tomcat_untar_dir, my_home)
    print '%s aaaaaaaaaaaaaaaaaaa' % dfile_name
    tomcat_dir = '/'.join([my_home, dfile_name[:-7]])
    os.environ['TOMCAT_HOME'] = tomcat_dir
    print 'sssssssssssssssssss %s ' % tomcat_dir
    #print '%s aaaaaaaaaaaaaaaaaaa' % dfile_name
    tomcat_dir = '/'.join([my_home, dfile_name[:-7]])
    os.environ['TOMCAT_HOME'] = tomcat_dir
    tomcat_dir = tomcat_dir
    #print 'sssssssssssssssssss %s ' % tomcat_dir
    tomcat_conf_file = '/'.join([tomcat_dir, 'conf', 'server.xml'])
    xitong.edit_file(tomcat_conf_file, 'port="8005"', 'port="-1"')
    xitong.edit_file(tomcat_conf_file, '<Connector port="8080" protocol="HTTP/1.1"','<Connector port="8081" protocol="org.apache.coyote.http11.Http11NioProtocol"')
	xitong.edit_file(tomcat_conf_file,'redirectPort="8443" />','redirectPort="8443" acceptCount="500" maxThreads="400"/>')
    xitong.edit_file(tomcat_conf_file, '<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />', '<!--<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />-->')
    xitong.edit_file(tomcat_conf_file, 'appBase="webapps"', 'appBase="../webapps"')
    setenv_file = ''.join([os.environ['JDK_UNTAR_DIR'], 'setenv.sh'])
    tomcat_bin_dir = '/'.join([tomcat_dir, 'bin'])
    shutil.move(setenv_file, tomcat_bin_dir)
    os.system('chown -R %s:%s %s' % (config.Config.user, config.Config.user, tomcat_dir))
    applypath1 = '/'.join([my_home, 'axinfu/config'])
    os.makedirs(applypath1)
    applypath2 = '/'.join([my_home, 'axinfu/cert'])
    os.makedirs(applypath2)
    applypath3 = '/'.join([my_home, 'axinfu/accountfile'])
    os.makedirs(applypath3)
    applypath4 = '/'.join([my_home, 'axinfu/mgrfilepath'])
    os.makedirs(applypath4)
    os.system('chown -R %s:%s /home/%s/axinfu' % (config.Config.user, config.Config.user,config.Config.user))
    tomserv_file = ''.join([os.environ['JDK_UNTAR_DIR'], 'tomcat'])
    tomcat_vername = os.environ['TOMCAT_VER']
    xitong.edit_file(tomserv_file, '7.0.73-all', tomcat_vername)
    xitong.edit_file(tomserv_file, 'pay', config.Config.user)
    shutil.move(tomserv_file, '/etc/init.d')
    src_webapps = ''.join(['/home/',config.Config.user,'/apache-tomcat-',url_back,'/webapps'])	
    des_webapps = '/'.join(['/home',config.Config.user,'webapps']) 
    shutil.move(src_webapps,des_webapps)
    if os_dist in ('centos', 'redhat'):
        subprocess.call('chkconfig --add tomcat' , shell=True)
    elif os_dist == 'Ubuntu' :
        subprocess.call('update-rc.d tomcat defaults', shell=True)



def mysql_back():
    if os_dist in ('centos', 'redhat', 'OracleServer'):
        percona_rpmurl = config.Config.PER_RPM_URL
        subprocess.call('rpm -ivh %s' % percona_rpmurl, shell=True)
        subprocess.call('yum install percona-xtrabackup', shell=True)
    elif os_dist == 'Ubuntu' :
        download(config.Config.PER_DEB_URL,'./percona.deb')
        subprocess.call('dpkg -i percona.deb', shell=True)
        subprocess.call('apt-get update', shell=True)
        subprocess.call('apt-get install percona-xtrabackup', shell=True)
    sql_list = ["create user '%s'@'%s' identified by '%s';" % ('bak', 'localhost', 'axfchonga'),
                "GRANT RELOAD, LOCK TABLES, REPLICATION CLIENT ON *.* TO '%s'@'%s';" % ('bak', 'localhost'),
                "FLUSH PRIVILEGES;"
                ]
    mysql_back_os_dist = platform.dist()[0]
    if mysql_back_os_dist in ('centos', 'redhat'):
        for sql in sql_list:	
            sql = 'mysql -uroot -e "%s"' % sql
            os.system(sql)
    else:
	for sql in sql_list:	
            sql = 'mysql -uroot -ppssesa -e "%s"' % sql
            os.system(sql)
    mysql_backup_py_dir = ''.join([os.environ['JDK_UNTAR_DIR'], 'mysql_back_up'])
    print mysql_backup_py_dir
    shutil.move(mysql_backup_py_dir ,config.Config.PWD)
    #crontab 怎么加?



