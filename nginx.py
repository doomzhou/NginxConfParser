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
    ServerStartFlag, ServerEndFlag, LocationStartFlag, LocationEndFlag = False, True, False, True
    server_name, location_name, backend_name = '', '', ''
    for nginx_file in [x for x in os.listdir(s) if os.path.isfile(os.path.join(s, x))]:
    # for nginx_file in ['bbs.91syt.com.conf']:
        for line in open(os.path.join(s, nginx_file), 'r').readlines():
            if re.match(r'^ *#.*', line):       # Ignore comment line
                continue
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
            # above upstream parser;below server parser
            if ServerStartFlag == False and ServerEndFlag == True \
                and LocationEndFlag == True and LocationStartFlag == False \
                and re.match(r'server {' ,line):
                ServerStartFlag = True
            elif ServerStartFlag == True and ServerEndFlag == True \
                and LocationEndFlag == True and LocationStartFlag == False \
                and re.match(r'^ *server_name .*;', line):
                m = re.search(r'^ *server_name +(.*);', line)
                server_name = m.group(1)
            elif ServerStartFlag == True and ServerEndFlag == True \
                and LocationEndFlag == True and LocationStartFlag == False\
                and re.match(r'^ *location .*{', line):
                LocationStartFlag = True
                m = re.search(r'^ *location +(.*) {', line)
                location_name = m.group(1)
            elif ServerStartFlag == True and ServerEndFlag == True \
                and LocationEndFlag == True and LocationStartFlag == True:
                if re.match(r'^ *proxy_pass *http://.*;', line):
                    m = re.search(r'^ *proxy_pass *http://(.*);', line)
                    backend_name = m.group(1)
                    backend_name = backend_name[:-1] if backend_name[-1] == '/' else backend_name
                    try:
                        backend_name = [x for x in UpstreamListDict if backend_name \
                                == x['upstream_name']][0]['upstream_servers']
                    except:
                        pass
                elif re.match(r'^ *root .*;', line):
                    m = re.search(r'^ *root +(.*);', line)
                    backend_name = m.group(1)
                elif re.match(r'^ *rewrite .*;', line):
                    m = re.search(r'^ *rewrite +(.*);', line)
                    backend_name = m.group(1)
                elif re.match(r'^ *}', line):
                    LocationStartFlag, LocationEndFlag = False, True
                    ServerListDict.append({
                        "server_name": server_name,
                        "location_name": location_name,
                        "backend_name": backend_name
                        })
            elif ServerStartFlag == True and ServerEndFlag == True \
                and LocationEndFlag == True and LocationStartFlag == False\
                and re.match(r'^ *}', line):
                LocationEndFlag = True
                ServerStartFlag, ServerEndFlag, LocationStartFlag, \
                    LocationEndFlag = False, True, False, True
    from pprint import pprint
    pprint(ServerListDict)

if __name__ == '__main__':
    pass
