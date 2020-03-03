#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import realpath,join,split
sitemap = join(split(realpath(__file__))[0],"sitemap")

def loadmap(src=sitemap):
    mapper = []
    for line in open(sitemap,"r"):
        mapper.append(line.strip("\r").strip("\n"))
    return mapper
        
if __name__ == '__main__':
    for i in loadmap():
        print(i)