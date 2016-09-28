#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from Foundation import NSData
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListMutableContainersAndLeaves
from workflow import Workflow


def searchPath(filepath, searchContents):
    """ 调用mdfind查找某个路径下的文件
    """
    commandline = u"mdfind -onlyin " + \
        filepath + u" " + u' '.join(searchContents)
    p = subprocess.Popen(commandline,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         close_fds=True)
    buffer = p.stdout.readlines()
    return buffer


def addToWf(wf, buffer, icon):
    for filename in buffer:
        filename = filename.strip(u"\r\n")
        plist_data = NSData.dataWithContentsOfFile_(filename)
        (dataObject, plistFormat, error) = (
            NSPropertyListSerialization.
            propertyListWithData_options_format_error_(
                plist_data,
                NSPropertyListMutableContainersAndLeaves,
                None,
                None))
        wf.add_item(title=dataObject["Name"],
                    subtitle=dataObject["URL"],
                    arg=dataObject["URL"],
                    valid=True,
                    icon=icon)

safari_dir = u"/Users/shaogaoyang/Library/Caches/Metadata/Safari/"
bookmarks_dir = u"Bookmarks"
history_dir = u"History"
fav_icon = u"./fav.png"
his_icon = u"./histroy.png"

wf = Workflow()

bookmarks_fullpath = os.path.join(safari_dir, bookmarks_dir)
history_fullpath = os.path.join(safari_dir, history_dir)

buffer = searchPath(bookmarks_fullpath, wf.args)
addToWf(wf, buffer, fav_icon)

buffer = searchPath(history_fullpath, wf.args)
addToWf(wf, buffer, his_icon)

wf.send_feedback()
