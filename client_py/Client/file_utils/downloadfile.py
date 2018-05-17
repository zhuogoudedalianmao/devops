#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import hashlib
import json
import os

import requests

import config
from log import gen_log


def getfilelist(school_code):
    """
    获取待下载文件列表信息
    :param school_code: 
    :return: 
    """
    try:
        url_filelist = '/'.join([config.Config.SERVER_URL, 'getFileList'])
        json_str = json.dumps({'code': school_code})
        sign_str = ''.join([json_str, config.Config.HASH_KEY])
        signature = hashlib.md5(sign_str).hexdigest()
        params = {"json": json_str,"signature": signature}
        r = requests.post(url_filelist,data=params)
        gen_log.info('getfilelist url: %s, params: %s, response: %s',
                     url_filelist, json.dumps(params, ensure_ascii=True), r.text)

        response = r.json()
        if response['respcode'] == '00':
            filelist = response['filelist']
            return filelist
        else:
            gen_log.error(u'调用获取文件列表接口失败：%s', response['respdesc'])
            return None
    except Exception:
        gen_log.exception(u'调用获取文件列表接口异常：')
        return None


def comparefilehash(file_name, file_hash):
    """
    尝试读取文件filename并计算文件的指纹，判断指纹是否匹配。
    匹配成功返回True，否则返回False
    :param file_name: 
    :param file_hash: 
    :return: 
    """
    if not os.path.isfile(file_name):
        return False
    else:
        md5 = hashlib.md5()
        with open(file_name, 'rb') as f:
            maxbuf = 8192
            while True:
                buf = f.read(maxbuf)
                if not buf:
                    break
                md5.update(buf)
        loc_hash = md5.hexdigest()
        if loc_hash == file_hash:
            return True
        else:
            return False


def downloadfile(school_code, file_id, filename):
    """
    下载指定文件
    :param school_code: 学校编码
    :param file_id: 文件ID
    :param filename: 本地文件名
    :return: 
    """
    try:
        url_fileinfo = '/'.join([config.Config.SERVER_URL, 'downloadFile'])
        json_str = json.dumps({'code': school_code, 'itemid': file_id})
        sign_str = ''.join([json_str, config.Config.HASH_KEY])
        signature = hashlib.md5(sign_str).hexdigest()
        params = {"json": json_str, "signature": signature}
        r = requests.post(url_fileinfo, data=params, stream=True)
        gen_log.info('downloadfile url: %s, params: %s, response: %s',
                     url_fileinfo, json.dumps(params, ensure_ascii=True), r.text)

        f = open(filename, "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return True
    except Exception:
        gen_log.exception('下载文件异常：')
        return False


def notifyfiledownloadstatus(school_code, file_id, downloadstatus):
    """
    返回下载成功与否的信息
    :param school_code: 
    :param file_id: 
    :param downloadstatus: 
    :return: 
    """
    try:
        url_notify = '/'.join([config.Config.SERVER_URL, 'notify'])
        json_str = json.dumps({'code':school_code, 'downloadstatus':downloadstatus, 'itemid':file_id})
        sign_str = ''.join([json_str, config.Config.HASH_KEY])
        signature = hashlib.md5(sign_str).hexdigest()
        params = {'json':json_str,'signature':signature}
        r = requests.post(url_notify,data=params)
        gen_log.info('downloadfile url: %s, params: %s, response: %s',
                     url_notify, json.dumps(params, ensure_ascii=True), r.text)
        responde = r.json()
        respondecode = responde["respcode"]
        if respondecode=="00":
            return True
        else:
            return False

    except Exception:
        gen_log.exception("通知异常:")
        return False



'''
if __name__=="__main__":
    filelist = getfilelist("88888")
    for i in range(len(filelist)):
        print filelist[i]
'''
