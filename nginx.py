#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File Name : nginx.py
'''Purpose : Intro sth                                 '''
# Creation Date : 1466596400
# Last Modified :
# Release By : Doom.zhou
###############################################################################

import re
import os
import sys
import logging

def NginxParse(s='lapp/nginx/file/site-enable_dir/'):
    if not os.path.isdir(s):
        logging.warning('args error')
        sys.exit(2)
    UpstreamListDict, ServerListDict = [], []
    UpstreamStartFlag, UpstreamEndFlag = False, False
    upstream_name, upstream_servers = '', ''
    ServerStartFlag, ServerEndFlag, LocationStartFlag, LocationEndFlag = False, False, False, False
    server_name, proxy_pass_name = '', ''
    # for nginx_file in [x for x in os.listdir(s) if os.path.isfile(os.path.join(s, x))]:
    for nginx_file in ['bbs.91syt.com.conf']:
        for line in open(os.path.join(s, nginx_file), 'r').readlines():
            if re.match(r'^ *upstream', line):
                UpstreamStartFlag = True
                m = re.search(r'^ *upstream +(.*) {', line)
                upstream_name = m.group(1)
            elif UpstreamStartFlag == True and UpstreamEndFlag == False \
                and re.match(r'^ *server ', line):
                m = re.search(r'^ *server +(.*);', line)
                upstream_servers += '%s ' % m.group(1)
            elif UpstreamStartFlag == True and UpstreamEndFlag == False \
                and re.match(r'^ *}', line):
                UpstreamStartFlag, UpstreamEndFlag = False, False
                UpstreamListDict.append({"upstream_name": upstream_name,
                    "upstream_servers": upstream_servers[:-1]})
                upstream_name, upstream_servers = '', ''
            if re.match(r'server {' ,line):
                ServerStartFlag = True
                print(line, end='')
            elif ServerStartFlag == True and ServerEndFlag == False \
                and re.match(r'^ *server_name .*;', line):
                print(line, end='')
            elif ServerStartFlag == True and ServerEndFlag == False \
                and re.match(r'^ *proxy_pass .*;', line):
                print(line, end='')
            elif ServerStartFlag == True and ServerEndFlag == False \
                and re.match(r'^ *}', line):
                LocationEndFlag = True
            elif ServerStartFlag == True and ServerEndFlag == False \
                and LocationEndFlag == True and re.match(r'^ *}', line):
                ServerEndFlag == True
                print(line, end='')


if __name__ == '__main__':
    NginxParse()
    pass
