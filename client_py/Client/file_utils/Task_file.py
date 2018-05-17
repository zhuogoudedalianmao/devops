#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from file_utils import downloadfile
import os
import config

def taskfile():
    filelist = downloadfile.getfilelist(config.Config.school_code)
    #print filelist
    #print type(filelist)
    for i in range(len(filelist)):
        fileinfo = filelist[i]
        filename = fileinfo['filename']
        filehash = fileinfo['filehash']
        file_id = fileinfo['itemid']

        # downloadloadstatus = "01"
        absfilename = os.path.join(config.Config.base_dir, filename)
        #print filename
	#print absfilename
        if downloadfile.comparefilehash(absfilename, filehash):
	    filename =  str(filename)
	    print filename
            print '文件 %s 不需要下载。' %filename
            for i in range(5):
                if downloadfile.notifyfiledownloadstatus(config.Config.school_code, file_id, '00'):
                    break
                else:
                    downloadfile.notifyfiledownloadstatus(config.Config.school_code, file_id, '00')
        else:
            if downloadfile.downloadfile(config.Config.school_code, file_id, absfilename):
                filename =  type(str(filename))
                print '文件 %s 下载成功。' %filename
                for i in range(5):
                    if downloadfile.notifyfiledownloadstatus(config.Config.school_code, file_id, '00'):
                        break
                    else:
                        downloadfile.notifyfiledownloadstatus(config.Config.school_code, file_id, '00')
            else:
                filename =  type(str(filename))
                print '文件 %s 下载失败。' %filename
                for i in range(5):
                    if downloadfile.notifyfiledownloadstatus(config.Config.school_code, file_id, '01'):
                        break
                    else:
                        downloadfile.notifyfiledownloadstatus(config.Config.school_code, file_id, '01')
