#!/usr/bin/python

# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout
import sys
import exceptions

scout.ScoutCore.load_all_modules()

def supress_keyborad_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(type, value, traceback):
        if type != exceptions.KeyboardInterrupt:
            old_excepthook(type, value, traceback)
        else:
            pass

    sys.excepthook = new_hook

supress_keyborad_interrupt_message()

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
