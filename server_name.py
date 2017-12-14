#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:10:01 2017

@author: kshitijbhatnagar
"""

import atexit
import logging
import os
import shelve
import web
import utils

#for mapping between directory name and file server
class NameService:
    #Return a server which hold the directory in which filepath is located.
    def GET(self, path):
    
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        path = str(path)

        if path == '/':
            return '\n'.join('%s=%s' % (directorypath, _name[directorypath])
                    for directorypath in sorted(_name))

        directorypath = str(os.path.dirname(path))

        if directorypath in _name:
            return _name[directorypath]

        raise web.notfound('No file server has this file.')


    def POST(self, directorypath):
        
        return _update(str(directorypath))

    def DELETE(self, directorypath):
        
        return _update(str(directorypath), False)


def _update(directorypath, add=True):
    
    web.header('Content-Type', 'text/plain; charset=UTF-8')
    j = web.input()

    if 'srv' not in j:
        raise web.badrequest()

    srv = j['srv']

    if directorypath == '/':
        if 'dirs' not in j:
            raise web.badrequest()

        for directorypath in j['dirs'].split('\n'):
            if not directorypath:
                continue

            try:
                _update_names(directorypath, srv, add)
            except ValueError as e:
                logging.exception(e)

    else:
        try:
            _update_names(directorypath, srv, add)
        except ValueError as e:
            logging.exception(e)


    return 'OK' 


def _update_names(directorypath, srv, add=True):
    
    if directorypath[-1] == '/':
        directorypath = os.path.directoryname(directorypath)

    if add:
        logging.info('Update directory %s on %s.', directorypath, srv)
        _name[directorypath] = srv

    elif directorypath in _name:
        logging.info('Remove directory %s on %s.', directorypath, srv)
        del _name[directorypath]

    else:
        raise ValueError('%s wasn\'t not deleted, because it wasn\'t'
                         ' in the dictionnary/database.' % directorypath)


_config = {
            'dbfile': 'names.db',
         }

logging.info('Loading config file nameserver.dfs.json.')
utils.load_config(_config, 'nameserver.dfs.json')
_name = shelve.open(_config['dbfile'])

atexit.register(lambda: _name.close())