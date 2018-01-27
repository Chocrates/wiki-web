#!/usr/bin/python3

import urllib.request
import urllib.parse
import logging
from bs4 import BeautifulSoup
from wikiNode import WikiNode


class Spider():
    logger = logging.getLogger('Wiki-web.spider')
    wiki_prefix = 'http://en.wikipedia.org'
    ignore_list = [
        'Main_Page', 'Wikipedia:', 'File:', 'Category:', 'Special:', 'Help:',
        'Portal:', 'Template:'
    ]

    def get_page(self, url):
        ''' Return the UTF-8 decoded HTML String of the passed in URL '''
        try:
            return urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
        except Exception as e:
            self.logger.error(e)
            raise

    def get_soup(self, page):
        ''' Extracting BS call to a passthrough method for easier testing '''
        try:
            return BeautifulSoup(page, 'lxml')
        except Exception as e:
            self.logger.error(e)
            raise

    def get_links(self, page, prefix):
        links = []
        soup = self.get_soup(page)
        for elem in soup.find_all('a', href=True):
            try:
                links.append(elem['href'] if bool(
                    urllib.parse.urlparse(elem['href']).netloc) else
                             prefix + elem['href'])
            except Exception as e:
                # Don't raise the exception so we can try and
                # get all of the links we can
                self.logger.error(e)

        return links

    def filter_links(self, links):
        return [
            link for link in links
            if self.wiki_prefix + '/wiki/' in link and not any(
                pattern in link for pattern in self.ignore_list)
        ]

    def build_node(self, link, parent=None, depth=1):
        if depth == 0:
            return WikiNode(link, self.build_title_from_url(link), parent, None)
        else:
            page = self.get_page(link)
            # Get the child links, cast to a set to remove duplicates
            # Sort so testing is easier for now
            child_links = sorted(
                set(self.filter_links(self.get_links(page, self.wiki_prefix))))
            node = WikiNode(link,
                            self.build_title_from_url(link),
                            parent, None)
            node.children = [
                self.build_node(child, node, depth - 1) for child in child_links
            ]
            return node

    def build_title_from_url(self, url):
        ''' Build a title from an english Wikipedia URL '''
        if 'http://en.wikipedia.org/wiki/' in url[:29]:
            return urllib.parse.unquote(url[29:].replace('_', ' '))
        else:
            self.logger.error('Invalid link provided: %s', url)
            raise ValueError('Invalid URL Provided')


    def get_wiki_body(self,url):
        soup = self.get_soup(self.get_page(url))
        for elem in soup.find_all('div'):
            if elem.get('id') == 'content':
                return str(elem)

        raise ValueError('content div for %s not found'.format(url))
