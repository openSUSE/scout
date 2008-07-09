#!/usr/bin/python

# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout

ret = scout.ScoutCore.run()
if ret != None:
    print ret
