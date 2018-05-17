#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import random

def getPort():
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    b = (set(procarr))
    t = random.randint(10000,50000)
    tt = str(t)
    if tt in b:
        getPort()
    else:
        print t

if __name__=='__main__':
    for i in range(2):
        getPort()
