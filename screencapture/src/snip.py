#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from workflow import Workflow

def main(wf):
    args = wf.args

    wf.logger.debug(args)

    if args[0] == u"":
        wf.add_item(title=u"截屏-拉框-剪贴板", subtitle=u"", arg=u"sniprecttoclip", valid=True)
        #wf.add_item(title=u"截屏-拉框-文件夹", subtitle=u"", arg=u"sniprecttofile", valid=True)
        wf.add_item(title=u"截屏-全屏-剪贴板", subtitle=u"", arg=u"sniptoclip", valid=True)
        #wf.add_item(title=u"截屏-全屏-文件夹", subtitle=u"", arg=u"sniptofile", valid=True)
        wf.send_feedback()
        return

    if args[0] == u"sniprecttoclip":
        os.system("screencapture -c -i")
    elif args[0] == u"sniptoclip":
        os.system("screencapture -c")

if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
