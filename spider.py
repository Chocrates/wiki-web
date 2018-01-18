#!/usr/bin/python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import sys
from wikiNode import WikiNode
import html

class Spider:
   wiki_prefix = 'http://en.wikipedia.org'
   ignore_list = [
         'Main_Page',
         'Wikipedia:',
         'File:',
         'Category:',
         'Special:',
         'Help:',
         'Portal:',
         'Template:'
   ]

   def getPage(self,url):
      try:
         return urllib.request.urlopen(url).read().decode('utf-8','ignore')
      except Exception as e:
         print(e)

   def getLinks(self,page,prefix):
      links = []
      soup = BeautifulSoup(page,'lxml')
      for elem in soup.find_all('a', href=True):
         try:
            links.append(elem['href'] if bool(urllib.parse.urlparse(elem['href']).netloc) else prefix + elem['href'])
         except ValueError:
            import pdb; pdb.set_trace()
      return links

   def filterLinks(self,links):
      return [link for link in links
               if self.wiki_prefix + '/wiki/' in link
               and not any(pattern in link for pattern in self.ignore_list)]

   def buildNode(self, link, parent = None, depth = 1):
      if depth == 0:
         return WikiNode(link,
                        # BeautifulSoup(self.getPage(link), 'lxml').title.string[:-12],
                         self.buildTitleFromUrl(link),
                         parent, None)
      else:
         page = self.getPage(link)
         # Get the child links, cast to a set to remove duplicates
         # Sort so testing is easier for now
         child_links = sorted(set(self.filterLinks(self.getLinks(page,self.wiki_prefix))))
         node = WikiNode(link, BeautifulSoup(page,'lxml').title.string[:-12], parent, None)
         node.children = [self.buildNode(child, node, depth - 1) for child in child_links]
         return node

   def buildTitleFromUrl(self, url):
      return urllib.parse.unquote(url[29:].replace('_',' '))

if __name__ == '__main__':
      depth = 1

#      wiki_nodes = buildNode('http://en.wikipedia.org/wiki/Great-tailed_grackle', depth)
      wiki_nodes = buildNode('http://en.wikipedia.org/wiki/John_Wesley_Hyatt',depth)
      for link in wiki_nodes:
         print(link)
