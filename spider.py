#!/usr/bin/python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import sys

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
      # return [link for link in links 
      #     if not any(re.match(link,pattern) for pattern in ignore_list)
      #         and wiki_prefix in link]

   def buildNode(self,links, depth = 1):
      link_list = links
      if type(links) is str:
         link_list = [links]

      if depth == 0:
         return link_list
      else:
         for link in link_list:
               page = self.getPage(link)
               # get the unique links without duplicates
               page_links = list(set(self.filterLinks(self.getLinks(page,self.wiki_prefix))) - set(link_list))
   #            import pdb; pdb.set_trace()
               return link_list + self.buildNode(page_links, depth - 1)



if __name__ == '__main__':
      depth = 1

      wiki_nodes = buildNode('http://en.wikipedia.org/wiki/Great-tailed_grackle', depth)
      for link in wiki_nodes:
         print(link)