#!/usr/bin/python

# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout
import sys

scout.ScoutCore.load_all_modules()

ret = scout.ScoutCore.run()
if ret != None:
    (empty, result) = ret
    if empty:
        sys.exit(3)
    else:
        print result,
    sys.exit(0)
else:
    sys.exit(4)
