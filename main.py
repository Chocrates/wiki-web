#!/usr/bin/python3

import sys
from spider import Spider

if __name__ == '__main__':
   depth = 1
   spider = Spider()
   wiki_nodes = spider.buildNode('http://en.wikipedia.org/wiki/Great-tailed_grackle', depth)
   for link in wiki_nodes:
      print(link)
