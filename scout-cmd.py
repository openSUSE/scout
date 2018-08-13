#!/usr/bin/python3

# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout
import sys

scout.ScoutCore.load_all_modules()


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(type, value, traceback):
        if type != KeyboardInterrupt:
            old_excepthook(type, value, traceback)
        else:
            pass

    sys.excepthook = new_hook


suppress_keyboard_interrupt_message()

ret = scout.ScoutCore.run()
if ret is not None:
    (empty, result) = ret
    if empty:
        sys.exit(3)
    else:
        print(result, end=' ')
    sys.exit(0)
else:
    sys.exit(4)
