#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: kshitijbhatnagar
"""

import random

import dfs.client

if __name__ == '__main__':
    with dfs.client.open('/wtf/42', 'a') as f:
        f.write('%6d\n' % random.randint(0, 10 ** 6))

        try:
            open('/wtf/42')
        except:
            print('Success')