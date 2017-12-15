#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: kshitijbhatnagar
"""

import json
import os.path

#Load the config file filename (JSON) if it exists and updates
def load_configuration(config, filepath):
    pass

#Return a tuple ('host', port) from the string s
def get_host_port(s):
    host, port = s.split(':')
    return host, int(port)


#lock server host:port if filepath is locked
def is_locked(filepath, host, port, lock_id=None):
    pass

#Return a server owning filepath.
def get_server(filepath, host, port):
    pass

#get a lock from the lockserver (host, port)
def get_lock(filepath, host, port):
    pass

#Revoke the lock on filepath
def revoke_lock(filepath, host, port, lock_id):
    pass


    
