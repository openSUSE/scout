#!/usr/bin/python

# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout

scout.ScoutCore.load_all_modules()

ret = scout.ScoutCore.run()
if ret != None:
    print ret
