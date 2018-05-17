#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import downloadfile

school_code = '88888'
base_dir = '/root/axinfu/'


def filecrontab():
    for fileinfo in downloadfile.getfilelist(school_code):
        filename = fileinfo['filename']
        fileurl = fileinfo['fileurl']
        filehash = fileinfo['filehash']
        file_id = fileinfo['itemid']

        #downloadloadstatus = "01"
        filename = os.path.join(base_dir, filename)
        if downloadfile.comparefilehash(filename, filehash):
            print '文件 %s 不需要下载。' % filename
            for i in range(5):
                if downloadfile.notifyfiledownloadstatus(school_code,file_id,'01'):
                    break
                else:
                    downloadfile.notifyfiledownloadstatus(school_code,file_id,'01')
        else:
            if downloadfile.downloadfile(school_code, file_id, filename):
                print '文件 %s 下载成功。' % filename
                for i in  range(5):
                    if downloadfile.notifyfiledownloadstatus(school_code, file_id, '00'):
                        break
                    else:
                        downloadfile.notifyfiledownloadstatus(school_code,file_id,'00')
            else:
                print '文件 %s 下载失败。' % filename
                for i in range(5):
                    if downloadfile.notifyfiledownloadstatus(school_code, file_id, '01'):
                        break
                    else:
                        downloadfile.notifyfiledownloadstatus(school_code,file_id,'01')

