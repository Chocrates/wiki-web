#!/usr/bin/python3

from spider import Spider
from window import TreeWindow

import sys
from gi.repository import Gtk
import signal
import logging
import gi
gi.require_version('Gtk', '3.0')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(relativeCreated)6d %(threadName)s %(message)s')

    # Enable SIGINT handling see:
    # https://bugzilla.gnome.org/show_bug.cgi?id=622084
    # https://stackoverflow.com/a/16486080/298149
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # depth probably should be deprecated at this point
    #  we used to want to grab the html for node children
    #  but that proved to be inefficient
    depth = 4
    spider = Spider()

    # Build the root node from argv[1] or default to grackles
    if len(sys.argv) == 2:
        wikiNodes = spider.buildNode(sys.argv[1], None, depth)
    else:
        wikiNodes = spider.buildNode(
            'http://en.wikipedia.org/wiki/Great-tailed_grackle', None, depth)

    TreeWindow(wikiNodes)
    Gtk.main()
