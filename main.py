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
import signal
import logging

if __name__ == '__main__':
   logging.basicConfig(level=logging.DEBUG,
      format='%(relativeCreated)6d %(threadName)s %(message)s')
   import signal
   signal.signal(signal.SIGINT, signal.SIG_DFL)

   # depth probably should be deprecated at this point
   # we used to want to grab the html for node children but that proved to be inefficient
   depth = 1 
   spider = Spider()

   # Build the root node from argv[1] or default to grackles
   if len(sys.argv) == 2:
      wikiNodes = spider.buildNode(sys.argv[1], None, depth)
   else:
      wikiNodes = spider.buildNode(
         'http://en.wikipedia.org/wiki/Great-tailed_grackle', None, depth)

   TreeWindow(wikiNodes)
   Gtk.main()

