#!/usr/bin/python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import sys
from wikiNode import WikiNode

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
         return urllib.request.urlopen(url).read()
      except urllib.error.HttpError as e:
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

#   def buildNode(self,links, depth = 1):
#      link_list = links
#      if type(links) is WikiNode:
#         link_list = [links]
#
#      if depth == 0:
#         return link_list
#      else:
#         for link in link_list:
#            page = self.getPage(link)
#            # get the unique links without duplicates
#            page_links = list(set(self.filterLinks(self.getLinks(page,self.wiki_prefix))) - set(link_list))
#            return WikiNode(link, link_list + self.buildNode(page_links, depth - 1), page)

   def buildNode(self, link, depth = 1):
      if depth == 0:
         return WikiNode(link, None, BeautifulSoup(self.getPage(link), 'lxml'))
      else:
         page = self.getPage(link)
         child_links = self.filterLinks(self.getLinks(page,self.wiki_prefix))[:8]
         return WikiNode(
            link,
            [self.buildNode(child, depth - 1) for child in child_links],
            BeautifulSoup(page,'lxml'))


if __name__ == '__main__':
      depth = 1

      wiki_nodes = buildNode('http://en.wikipedia.org/wiki/Great-tailed_grackle', depth)
      for link in wiki_nodes:
         print(link)
