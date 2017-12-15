#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kshitijbhatnagar
"""
import os.path
import datetime
import utility
import atexit
import collections
import logging
import shelve


Lock = collections.namedtuple('Lock', 'lock_id  which was granted ')


class LockServer:
    def GET(self, filepath):
        pass
    
    def POST(self, filepath):
        pass
    
    def DELETE(self, filepath):
        pass
   
    
def _lock_expired(filepath):
    last_used = _locks[filepath].last_used
    return (datetime.datetime.now() - last_used).seconds\
            > _config['lock_lifetime']    
            
def _check_new_lock(filepath):
    pass

def _update_lock(filepath):
    t = datetime.datetime.now()

    logging.info('Update lock on %s from %s to %s.',
                 filepath, _locks[filepath].last_used, t)

    l = _locks[filepath]
    l = Lock(l.lock_id, l.granted, t)
    _locks[filepath] = l


def _revoke_lock(filepath):
    pass


_config = {
            'dbfile': 'locks.db',
            'lock_lifetime': 60,
         }

logging.info('Loading config file lockserver.dfs.json.')
utility.load_config(_config, 'lockserver.dfs.json')
_locks = shelve.open(_config['dbfile'])

atexit.register(lambda: _locks.close())            