from spider import Spider
from wikiNode import WikiNode
from hamcrest import *
import unittest
from mock import MagicMock, patch
from urllib.error import URLError
import enum


class TestSpider(unittest.TestCase):
    '''
    Tests the Spider class and methods
    '''
    def setUp(self):
        self.spider = Spider()

    @patch('urllib.request.urlopen')
    def test_get_page_calls_url_open(self, mock_open):
        ''' Validate that we are calling the module with the passed in URL'''
        self.spider.get_page('test')
        mock_open.assert_called_with('test')


    @patch('spider.Spider.logger.error') # Remember the mock vars are in reverse order
    @patch('urllib.request.urlopen')
    def test_get_page_raises_exception(self, mock_open,mock_logger):
        ''' Validate that get_page() logs and rethrows the exception'''
        mock_open.side_effect = URLError('Test Exception')

        assert_that(calling(self.spider.get_page).with_args('test'),raises(URLError))
        mock_logger.assert_called()
        

    @patch('bs4.BeautifulSoup.__init__')
    def test_get_soup_calls_bs4_init(self, mock_soup):
        ''' Validate that we are calling the module with the passed in URL'''
        mock_soup.return_value = None
        self.spider.get_soup('test')

        # We want to validate that soup was called with 'test'
        # But we don't want the test to rely on the 'lxml' parser
        # Erring on the side of a slightly fragile test
        mock_soup.assert_called_with('test','lxml')


    @patch('spider.Spider.logger.error') 
    @patch('bs4.BeautifulSoup.__init__')
    def test_get_soup_raises_exception(self, mock_soup,mock_logger):
        ''' Validate that get_soup() logs and rethrows the exception'''
        # In reality this would be an HTMLParser.HTMLParseError or something
        # But instead of including all those dependencies, lets just validate
        # That is passes through the exception
        mock_soup.side_effect = ValueError('Test Exception')

        assert_that(calling(self.spider.get_soup).with_args('test'),raises(ValueError))
        mock_logger.assert_called()
        

    @patch('urllib.parse.urlparse')
    @patch('bs4.element.Tag.find_all')
    @patch('spider.Spider.get_soup')
    @patch('spider.Spider.logger.error') 
    def test_get_links_with_absolute_link_returns_page_links(self, mock_logger,mock_soup,mock_find_all, mock_parse):
        ''' Mock the external calls and verify that it doesn't prepend the suffix '''
        _prefix = 'test'
        pages = ['page_one', 'page_two']

        # Mock bs4 and make sure that it has a find_all method that returns an iterable
        mock_soup().find_all.return_value = [{'href':page} for page in pages]

        # Mock urlparse and make sure that it claims that we have an absolute link
        mock_parse().netloc = True

        out = self.spider.get_links('page',_prefix)
        assert_that(out, is_(equal_to(pages)))


    @patch('urllib.parse.urlparse')
    @patch('bs4.element.Tag.find_all')
    @patch('spider.Spider.get_soup')
    @patch('spider.Spider.logger.error') 
    def test_get_links_with_relative_link_returns_page_links(self, mock_logger,mock_soup,mock_find_all, mock_parse):
        ''' Mock the external calls and verify that it prepends the suffix if it is a rlative URL'''
        _prefix = 'test'
        pages = ['page_one', 'page_two']

        # Mock bs4 and make sure that it has a find_all method that returns an iterable
        mock_soup().find_all.return_value = [{'href':page} for page in pages]

        # Mock urlparse and make sure that it claims that we have an absolute link
        mock_parse().netloc = False

        out = self.spider.get_links('page',_prefix)
        assert_that(out, is_(equal_to([_prefix + x for x in pages])))


    @patch('urllib.parse.urlparse')
    @patch('bs4.element.Tag.find_all')
    @patch('spider.Spider.get_soup')
    @patch('spider.Spider.logger.error') 
    def test_get_links_with_invalid_link_logs_exception(self, mock_logger,mock_soup,mock_find_all, mock_parse):
        ''' Mock the external calls and verify that URLLib errors are logged and not thrown'''
        _prefix = 'test'
        pages = ['page_one', 'page_two']

        # Mock bs4 and make sure that it has a find_all method that returns an iterable
        mock_soup().find_all.return_value = [{'href':page} for page in pages]

        # Mock urlparse and make sure that it claims that we have an absolute link
        mock_parse.side_effect = ValueError('')
        out = self.spider.get_links('page',_prefix)
        assert_that(out, is_(equal_to([]))) # In this case all links are going to fail
        mock_logger.assert_called() # Validate that we logged the exception

    def test_filter_links_filters_on_prefix(self):
        ''' Test that filter_links will fileter out the invalid links '''
        _prefix = 'abc'
        urls = ['abc/wiki/1', 'abc/wiki/2', '3', 'any_other/domain/abc']
        self.spider.wiki_prefix = _prefix
        filtered_links = self.spider.filter_links(urls)

        assert_that(filtered_links,is_(equal_to(['abc/wiki/1', 'abc/wiki/2'])))



    @patch('urllib.parse.unquote')
    def test_build_title_from_url_returns_title(self, mock_parse):
        ''' Mock urllib and ensure that we call it with the last part of the URL'''
        self.spider.build_title_from_url('http://en.wikipedia.org/wiki/_test_name_')
        mock_parse.assert_called_with(' test name ')


    @patch('spider.Spider.logger.error') 
    def test_build_title_from_url_with_invalid_url_raises_valueerror(self, mock_logger):
        ''' Mock urllib and ensure any other URL raises an error and logs it'''
        assert_that(calling(self.spider.build_title_from_url).with_args('any other title really '),raises(ValueError))
        mock_logger.assert_called()
        
    def test_build_node_with_0_depth_returns_node(self):
        ''' Ensure that create a node with no children correctly'''
        url = 'http://en.wikipedia.org/wiki/title'
        expected_node = WikiNode(url,'title',None)
        returned_node = self.spider.build_node(url, None, 0)
        assert_that(returned_node, is_(equal_to(expected_node)))

    @patch('spider.Spider.filter_links')
    @patch('spider.Spider.get_links')
    @patch('spider.Spider.get_page')
    @patch('spider.Spider.get_soup')
    def test_build_node_with_1_depth_calls_build_node_on_children(self, mock_soup, mock_page, mock_links, mock_filter):
        ''' Ensure that we recursively call build_node on children and build the node correctly'''
        urls = {'title':'http://en.wikipedia.org/wiki/title',
                'b':'http://en.wikipedia.org/wiki/b',
                'a':'http://en.wikipedia.org/wiki/a'}

        expected_node = WikiNode(urls['title'],'title','parent')
        expected_child_a = WikiNode(urls['a'],'a',expected_node)
        expected_child_b = WikiNode(urls['b'],'b',None)
        expected_node.children = [expected_child_a, expected_child_b]

        mock_filter.return_value = [urls['b'], urls['a']]

        returned_node = self.spider.build_node(urls['title'], 'parent', 1)
        assert_that(returned_node, is_(equal_to(expected_node)))
