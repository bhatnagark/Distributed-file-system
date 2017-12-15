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

import utils

class FileServer:
   

    def GET(self, filepath):
        pass
    

    def PUT(self, filepath):
        pass
    
    
    def DELETE(self, filepath):
        pass
    
    def HEAD(self, filepath):
        pass

def _get_local_path(filepath):
    
    return os.path.join(os.getcwd(), _config['fsroot'], filepath[1:])


def _raise_if_locked(filepath):
    pass

def _raise_if_dir_or_not_servable(filepath):
   pass

def _raise_if_not_exists(filepath):
    pass

def _init_file_server():
    """Just notify the nameserver about which directories we serve."""

    host, port = utils.get_host_port(_config['server_name'])
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

# just to speed up the search to know if we can serve a file
# O(n) → O(log n)
_config['directories'] = set(_config['directories'])

_init_file_server()

