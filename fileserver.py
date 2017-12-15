#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: kshitijbhatnagar
"""

import logging
import os.path
import time

from contextlib import closing
from httplib import HTTPConnection

import web

import utility

class FileServer:
   

    def GET(self, filepath):
        web.header('Content-Type', 'text; char=UTF-8')

        dir_not_servable(path)
        dir_not_exist(path)
        if_locked(path)
        p = local_path(path)
        web.header('Last Modified', time.ctime(os.path.getmtime(p)))
        with open(p) as f:
            return f.read()
    

    def PUT(self, path):
        dir_not_servable(path)
        if_locked(path)
        p =local_path(path)
        with open(p, 'w') as f:
            f.write(web.data())
        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        return ''
    
    
    def DELETE(self, path):
        web.header('Content-Type', 'text; char=UTF-8')
        dir_not_servable(path)
        dir_not_exist(path)
        if_locked(path)
        os.unlink(local_path(path))
        return 'OK'
    
    def HEAD(self, path):
        web.header('Content-Type', 'text; char=UTF-8')
        dir_not_servable(path)
        dir_not_exist(path)
        if_locked(path)
        p = local_path(path)
        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        return ''

def local_path(path):
    
    return os.path.join(os.getcwd(), _config['fsroot'], path[1:])


def if_locked(path):
    j = web.input()
    host, port = utility.get_host_port(_config['lockserver'])
    if utility.is_locked(path, host, port, j.get('lock_id', None)):
        raise web.unauthorized()

def dir_not_servable(path):
   p = local_path(path)
    if (os.path.dirname(path) not in _config['directories'] or
            os.path.isdir(p)):
        raise web.notacceptable()

def dir_not_exist(path):
    p = local_path(path)
    if not os.path.exists(p):
        raise web.webapi.HTTPError('No Content',
                                   {'Content-Type': 'plain'})

def _init_file_server():
    host, port = utility.get_host_port(_config['server_name'])
    with closing(HTTPConnection(host, port)) as con:
        data = 'srv=%s&dirs=%s' % (_config['srv'],
                                '\n'.join(_config['directories']),)
        con.request('POST', '/', data)


_config = {
        'lockserver': None,
        'server_name': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
        }

logging.info('Loading config file fileserver.dfs.json.')
utils.load_config(_config, 'fileserver.dfs.json')
_config['directories'] = set(_config['directories'])
_init_file_server()

