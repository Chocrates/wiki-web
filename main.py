#!/usr/bin/python3

from spider import Spider
from window import TreeWindow

import sys
from gi.repository import Gtk
import signal
import logging
import gi
gi.require_version('Gtk', '3.0')
_DEFAULT_URL = 'http://en.wikipedia.org/wiki/Great-tailed_grackle'
def is_valid_url(url):
    # Using a complex REGEX may be overkill at this point
    # So we just validate that the begining part of the URL is valid
    # and part of Wikipedia english site
    return url[:29] == 'http://en.wikipedia.org/wiki/'

def get_nodes(spider,url_validator, arguments):
    # depth probably should be deprecated at this point
    #  we used to want to grab the html for node children
    #  but that proved to be inefficient
    depth = 1

    # Build the root node from argv[1] or default to grackles
    if len(arguments) > 2:
        raise ValueError('Too many arguments given')
    elif len(arguments) == 2:
        if url_validator(arguments[1]):
            return spider.build_node(arguments[1], None, depth)
        else:
            raise ValueError('Invliad URL given')
    else:
        return spider.build_node(
        _DEFAULT_URL, None, depth)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(relativeCreated)6d %(threadName)s %(message)s')

    # Enable SIGINT handling see:
    # https://bugzilla.gnome.org/show_bug.cgi?id=622084
    # https://stackoverflow.com/a/16486080/298149
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    wiki_nodes = get_nodes(Spider(),is_valid_url, sys.argv)

    TreeWindow(wiki_nodes)
    Gtk.main()
