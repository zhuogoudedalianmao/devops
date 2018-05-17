#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import sys

def ssh():
    #a = os.system("ssh root@192.168.0.194 'python poo.py'")
    b = os.popen("ssh root@192.168.0.193 'python poo.py'").read()
    c = b.split("\n")
    d = c[1]
    print c
    print d
    #return c[0]
    os.system('ssh -fCNR %s:localhost:22 root@192.168.0.193' %c[0])

if __name__=="__main__":
    port = ssh()
    print port
