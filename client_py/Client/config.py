#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import platform

class Config(object):
    def __init__(self):
        super(Config, self).__init__()

    basedir = os.path.abspath(os.path.dirname(__file__))
    base_dir = '/'.join([basedir,"axinfu/upload"])

    LOGGING = 'debug'
    LOG_TO_STDERR = True
    LOG_FILE_PREFIX = os.path.join(basedir, 'app.txt')
    LOG_FILE_MAX_SIZE = 100 * 1000 * 1000
    LOG_FILE_NUM_BACKUPS = 10
    SERVER_URL = 'http://182.139.182.234:8096/mr/publish'
    HASH_KEY = 'axinfu'
    school_code = "88888"

    PWD = os.path.abspath(os.path.dirname(__file__))
    TOMCAT_PATH = "/home/axinfu/tomcat.py"
    JDK_URL= 'http://182.139.182.234:8082/examples/jdk.tar.gz'
    REDIS_URL = 'http://download.redis.io/redis-stable.tar.gz'
    TOMCAT_URL = 'http://mirrors.tuna.tsinghua.edu.cn/apache/tomcat/tomcat-7/'
    PER_RPM_URL = 'http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm'
    ubuntu_codename = platform.dist()[2]
    PER_DEB_URL = ''.join(['https://repo.percona.com/apt/percona-release_0.1-4.', ubuntu_codename, '_all.deb'])
    JDK_GZ_PATH = ''.join([PWD, '/jdk.tar.gz'])
    user = 'axinfu'
