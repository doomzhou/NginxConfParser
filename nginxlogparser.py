#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : nginxlogparser.py
'''Purpose : 分析nginx 日志
log_format main '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] '
    '"$host" "$request" $status $bytes_sent '
    '"$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr" ';
'''
# Creation Date : 1466988979
# Last Modified :
# Release By : Doom.zhou
###############################################################################


import os, sys
import logging
import glob
from datetime import datetime, timedelta
from timeit import timeit


request_time, remote_addr, http_referer, time_local, request, bytes_sent, \
status, http_user_agent, host ='', '', '', '', '', '', '', '', ''

def logparser(logpath):
    with open(logpath, 'r') as f:
        lines = f.readlines()
    # handle the line of log
    result = []
    for line in lines:
        FirstSplitList = line.split('"')
        http_referer = FirstSplitList[5]
        FirstSplitList0 = FirstSplitList[0].split()
        FirstSplitList4 = FirstSplitList[4].split()
        request_time = FirstSplitList0[0]
        time_local = datetime.strptime((FirstSplitList0[-2]),
            '[%d/%b/%Y:%H:%M:%S')
        request = FirstSplitList[3]
        [status, bytes_sent] = FirstSplitList4
        host = FirstSplitList[1]
        http_user_agent = FirstSplitList[7]
        if FirstSplitList[0].find(',') == -1:
            remote_addr = FirstSplitList0[2]
        else:
            remote_addr = FirstSplitList0[3]
        result.append([request_time, remote_addr, http_referer, time_local,
                request, bytes_sent, status, http_user_agent, host])
    return result


if __name__ == '__main__':
    # test s='/path/to/nginx_log_dir/'
    result = logparser('/home/doom/tmp/logs/1.log')
    pass
