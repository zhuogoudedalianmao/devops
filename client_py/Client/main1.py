#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import argparse
from file_utils.Task_file import taskfile
from system_utils.Task_system import tasksystem
import config


task_list = {
    'init': tasksystem,
    'auto': taskfile
}


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("func",choices=['init', 'auto'], help="init--SYSTEM auto--taskfile")
    args = parser.parse_args()
    func_name = args.func
    if func_name in task_list:
        task = task_list[func_name]
        task()
    else:
        print "%s undefined." % func_name
