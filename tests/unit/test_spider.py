import spyder
from hamcrest import *
import unittest


class TestSpider(unittest.TestCase):
    '''
    Tests the Spider class and methods
    '''

    def test_2_arguments_with_url_returns_url(self):
        ''' Test that we call spider with the URL when we pass in a single command line arg '''
        _url = 'https://en.wikipedia.org/wiki/Austin,_Texas'

        result_url, result_parent, result_depth = main.getNodes(spiderStub,trueUrlValidatorStub,['main.py',_url])

        assert_that(result_url, equal_to(_url))
        assert_that(result_parent, equal_to(None))
        assert_that(result_depth, equal_to(1))
