#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Foundation import NSData
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListMutableContainersAndLeaves
from workflow import Workflow
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import Tokenizer, Token
from whoosh.qparser import QueryParser

class ChineseTokenizer(Tokenizer):

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)

        seglist = jieba.cut(value, cut_all=False)

        for w in seglist:
            t.orginal = t.text = w
            t.boost = 1.0
            if positions:
                t.pos = start_pos + value.find(w)
            if chars:
                t.start_char = start_char + value.find(w)
                t.endchar = start_char + value.find(w) + len(w)
            yield t


def ChineseAnalyzer():
    return ChineseTokenizer()

analyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
ix = create_in("indexdir", schema)
writer = ix.writer()

safari_dir = "/Users/shaogaoyang/Library/Caches/Metadata/Safari/"
bookmarks_dir = "Bookmarks"
history_dir = "History"

wf = Workflow()

bookmarks_fullpath = os.path.join(safari_dir, bookmarks_dir)
history_fullpath = os.path.join(safari_dir, history_dir)

for dirpath, dirnames, filenames in os.walk(history_fullpath):
    for filename in filenames:
        if os.path.splitext(filename)[1] == ".webhistory":
            plist_data = NSData.dataWithContentsOfFile_(
                os.path.join(history_fullpath, filename)
            )
            (dataObject, plistFormat, error) = (
                NSPropertyListSerialization.
                propertyListWithData_options_format_error_(
                    plist_data,
                    NSPropertyListMutableContainersAndLeaves,
                    None,
                    None))
            if "Full Page Text" in dataObject.keys():
                writer.add_document(title=dataObject["Name"],
                                    path=dataObject["URL"],
                                    content=dataObject["Full Page Text"])
            else:
                writer.add_document(title=dataObject["Name"],
                                    path=dataObject["URL"],
                                    content=dataObject["Name"])

writer.commit()

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(wf.args[0])
    results = searcher.search(query)
    print results
    for i in results:
        print i["path"]
        print i["title"]
                                


