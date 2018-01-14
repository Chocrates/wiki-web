#!/usr/bin/python3

import sys
import resource
from spider import Spider
from window import TreeWindow
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import pickle
import os

if __name__ == '__main__':
   depth = 3
   spider = Spider()
   fileName = 'wikiNodes.pkl'
   if os.path.isfile(fileName):
      with open(fileName, 'rb') as input:
         wikiNodes = pickle.load(input)
   else:
      wikiNodes = spider.buildNode('http://en.wikipedia.org/wiki/Great-tailed_grackle', depth)
      with open(fileName, 'wb') as output:
         max_rec = 0x100000
         resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
         sys.setrecursionlimit(max_rec) # Should try and determine a good value for this based on system memory
         pickle.dump(wikiNodes, output, pickle.HIGHEST_PROTOCOL)

#   for link in wiki_nodes:
#      import pdb; pdb.set_trace()
#      [print(x) for x in link]
#      print(str(link))
   TreeWindow(wikiNodes)
   Gtk.main()

