#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: kshitijbhatnagar
"""

import web

import dfs.lockserver

urls = (
        '(127.0.0.1',
       )

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()