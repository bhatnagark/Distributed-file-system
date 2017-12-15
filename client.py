#!/usr/bin/env python3
# -*- coding: utf-8 ''''


from contextlib import closing
from httplib import HTTPConnection
from tempfile import SpooledTemporaryFile

import utils

class File(SpooledTemporaryFile):
    
    def __init__(self, path, mode='rtc'):
        
        self.mode = mode
        self.path = path
        host, port = utils.get_host_port(_config['nameserver'])
        self.srv = utils.get_server(path, host, port)

        if self.srv is None:
            pass
        
        self.last_modified = None
        SpooledTemporaryFile.__init__(self, _config['max_size'], mode.replace('c', ''))

        host, port = utils.get_host_port(_config['lockserver'])
        if utils.is_locked(path, host, port):
            pass
        
        if 'w' not in mode:
            host, port = utils.get_host_port(self.srv)
            with closing(HTTPConnection(host, port)) as con:
                con.request('GET', path)
                response = con.getresponse()
                self.last_modified = response.getheader('Last-Modified')
                status = response.status


                if status != 204:
                    self.write(response.read())

                if 'r' in mode:
                    self.seek(0)

                self.lock_id = None

        if 'a' in mode or 'w' in mode:
            host, port = utils.get_host_port(_config['lockserver'])
            self.lock_id = int(utils.get_lock(path, host, port))

        if 'c' in mode:
            File._cache[path] = self

    
    def __exit__(self, exc, value, tb):
        
        self.close()

        if 'c' not in self.mode:
            return SpooledTemporaryFile.__exit__(self, exc, value, tb)

        return False

    def close(self):
        
        self.flush()

        if 'c' not in self.mode:
            SpooledTemporaryFile.close(self)

    def flush(self):
        
        SpooledTemporaryFile.flush(self)
        self.commit()

    def commit(self):
        if 'a' in self.mode or 'w' in self.mode:
          
            self.seek(0)
            data = self.read()
            host, port = utils.get_host_port(self.srv)
            with closing(HTTPConnection(host, port)) as con:
                con.request('PUT', self.path + '?lock_id=%s' % self.lock_id,
                            data)

                response = con.getresponse()
                self.last_modified = response.getheader('Last-Modified')
                status = response.status
                if status != 200:
                    pass
                
        if self.lock_id is not None:
            host, port = utils.get_host_port(_config['lockserver'])
            utils.revoke_lock(self.path, host, port, self.lock_id)
    
def unlink(path, lock_id=None):
    host, port = utils.get_host_port(_config['nameserver'])
    
    fs = utils.get_server(path, host, port)
    host, port = utils.get_host_port(fs)

    with closing(HTTPConnection(host, port)) as con:
        con.request('DELETE', path + '?lock_id=%s' % lock_id)

        status = con.getresponse().status

        if status != 200:
            pass
        
def rename(path, newfilepath):
    with open(path) as f:
        with open(newfilepath, 'w') as nf:
            nf.write(f.read())

        unlink(path, f.lock_id)


open = File

_config = {
        'server_name': None,
        'lockserver': None,
        'max_size': 1024 ** 2,
         } # default
File._cache = {}
utils.load_config(_config, 'client.dfs.json')    