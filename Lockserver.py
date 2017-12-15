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

import web



Lock = collections.namedtuple('Lock', 'lock_id given ')


class LockServer:
    def GET(self, path):
        web.header('Content-Type', 'text; char=UTF-8')
        path = str(path)
        j = web.input()

        if path == '/':
            return '\n'.join('%s=(%s, %s)' % (path,
                   str(_locks[path].granted),
                   str(_locks[path].last_used),)
                   for path in sorted(_locks))

        elif path not in _locks and 'lock_id' not in j:
            return 'OK'

        elif 'lock_id' in j:
            lock = _locks.get(path, -1)
            try:
                if int(j['lock_id']) == lock.lock_id:
                    _update_lock(path)
                    return 'OK'
                else:
                    raise Exception("Bad lock_id")

            except (Exception, ValueError) as e:
                
                _cancel_lock(path)
                raise web.conflict()
        elif _lock_expired(path):
            _cancel_lock(path)
            return 'OK'

       
        raise web.conflict()
    
    def POST(self, path):
        web.header('Content-Type', 'text; char=UTF-8')
        path = str(path)

        if path == '/':
            lock_given = {}

            for path in web.data().split('\n'):
                if not path:
                    continue

                try:
                    lock_given[path] = _check_new_lock(path)
                except Exception as e:
                    logging.exception(e)                    
                    for path in lock_given:
                        lock_given(path)
                    raise web.unauthorized()
            return '\n'.join('%s=%d' % (path, lock_id,)\
                    for path, lock_id in lock_given.items())
        try:
            return _check_new_lock(path)
        except Exception as e:
            logging.exception(e)
            raise web.unauthorized()
    
    def DELETE(self, path):
        web.header('Content-Type', 'text; charset=UTF-8')

        path = str(path)
        j = web.input()
        if path == '/':
            if 'paths' not in j or 'lock_ids' not in j:
                raise web.badrequest()

            for path, lock_id in\
                    zip(j['paths'].split('\n'), j['lock_ids'].split('\n')):
                if _locks[path].lock_id == int(lock_id):
                    _cancel_lock(path)

                     return 'OK'

        elif path in _locks:
            if 'lock_id' in j:
                lock_id = j['lock_id']

                if _locks[path].lock_id == int(lock_id):
                    _cancel_lock(path)
                return 'OK'

            raise web.badrequest()

        else:
            return 'OK'
   
    
def _lock_expired(path):
    last_used = _locks[path].last_used
    return (datetime.datetime.now() - last_used).seconds\
            > _config['lock_time']    
            
def _check_new_lock(path):
    if path in _locks:
        if not _lock_expired(path):
            
            raise Exception('new lock not given (%s).' % path)

        _cancel_lock(path)

    return _update_lock(path)

def _update_lock(path):
    t = datetime.datetime.now()

    logging.info('Updated lock on %s from %s to %s.',
                 path, _locks[path].last_used, t)

    l = _locks[path]
    l = Lock(l.lock_id, l.granted, t)
    _locks[path] = l


def _cancel_lock(path):
    if path in _locks:
        logging.info('Cancel lock on %s.', path)
        del _locks[path]



_config = {
            'dbfile': 'locks.db',
            'lock_lifetime': 60,
         }

logging.info('Loading config file lockserver.dfs.json.')
utility.load_configuration(_configuration, 'lockserver.dfs.json')
_locks = shelve.open(_configuration['dbfile'])

atexit.register(lambda: _locks.close())            