#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import platform
from system_utils import xitong


def tasksystem():
    os_dist = platform.dist()[0]
    os_ver = platform.dist()[1].split('.')[0]
    if os_dist in ('centos', 'redhat') and os_ver == '6':
        xitong.cxitong()
    elif os_dist == 'Ubuntu' and os_ver == '14':
        xitong.uxitong()
    else:
        print "\nThis script only support CentOS6, Ubuntu14.\nexit!\n"
        sys.exit()

