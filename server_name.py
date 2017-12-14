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

        raise web.notfound('No file server serve this file.')


    def POST(self, directorypath):
        """See _update (with add=True)."""

        return _update(str(directorypath))

    def DELETE(self, directorypath):
        """See _update (with add=False)."""

        return _update(str(directorypath), False)