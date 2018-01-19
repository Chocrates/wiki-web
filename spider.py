#!/usr/bin/python3

import urllib.request
import urllib.parse
import logging
from bs4 import BeautifulSoup
from wikiNode import WikiNode


class Spider(_UrlLib, ):
    wiki_prefix = 'http://en.wikipedia.org'
    ignore_list = [
        'Main_Page', 'Wikipedia:', 'File:', 'Category:', 'Special:', 'Help:',
        'Portal:', 'Template:'
    ]

    def __init__(self):
        self.logger = logging.getLogger('Wiki-web.window.TreeWindow')

    def getPage(self, url):
        try:
            return urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
        except Exception as e:
            print(e)

    def getLinks(self, page, prefix):
        links = []
        soup = BeautifulSoup(page, 'lxml')
        for elem in soup.find_all('a', href=True):
            try:
                links.append(elem['href'] if bool(
                    urllib.parse.urlparse(elem['href']).netloc) else
                             prefix + elem['href'])
            except ValueError as e:
                # Should we really just log here?
                # Or should we crash if we can't read links from a page?
                self.logger.error(e)

        return links

    def filterLinks(self, links):
        return [
            link for link in links
            if self.wiki_prefix + '/wiki/' in link and not any(
                pattern in link for pattern in self.ignore_list)
        ]

    def buildNode(self, link, parent=None, depth=1):
        if depth == 0:
            return WikiNode(link, self.buildTitleFromUrl(link), parent, None)
        else:
            page = self.getPage(link)
            # Get the child links, cast to a set to remove duplicates
            # Sort so testing is easier for now
            child_links = sorted(
                set(self.filterLinks(self.getLinks(page, self.wiki_prefix))))
            node = WikiNode(link,
                            BeautifulSoup(page, 'lxml').title.string[:-12],
                            parent, None)
            node.children = [
                self.buildNode(child, node, depth - 1) for child in child_links
            ]
            return node

    def buildTitleFromUrl(self, url):
        ''' Build a title from an english Wikipedia URL '''
        if 'http://en.wikipedia.org/wiki/' in url[:29]:
            return urllib.parse.unquote(url[29:].replace('_', ' '))
        else:
            self.logger.error('Invalid link provided: %s', url)
