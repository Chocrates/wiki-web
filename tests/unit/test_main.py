import main
from hamcrest import *
import unittest


# Build a passthrough Spider stub
# If we do this a lot, find a stub or mock framework
#  and move to a generic location
spider_stub = type('',(object,),{})()
spider_stub.build_node = lambda x, y, z: (x, y, z)

true_url_validator_stub = lambda x: True
false_url_validator_stub = lambda x: False

class TestMain(unittest.TestCase):
    '''
    Test that we parse the arguments correclty
    and that we call Spider when we need to with the correct arguments
    '''
    def test_2_arguments_with_url_returns_url(self):
        ''' Test that we call spider with the URL when we pass in a single command line arg '''
        _url = 'https://en.wikipedia.org/wiki/Austin,_Texas'

        result_url, result_parent, result_depth = main.get_nodes(spider_stub,true_url_validator_stub,['main.py',_url])

        assert_that(result_url, equal_to(_url))
        assert_that(result_parent, equal_to(None))
        assert_that(result_depth, equal_to(1))

    def test_1_argument_returns_default_url(self):
        ''' Tests that when we call the script by itself, we still get a page '''
        _url = 'https://en.wikipedia.org/wiki/Great-tailed_grackle'

        result_url, result_parent, result_depth = main.get_nodes(spider_stub,true_url_validator_stub,['main.py',_url])

        assert_that(result_url, equal_to(_url))
        assert_that(result_parent, equal_to(None))
        assert_that(result_depth, equal_to(1))

    def test_3_arguments_throws_value_error(self):
        ''' Tests that when we call the script by with too many args we get an exception '''
        _url = 'https://en.wikipedia.org/wiki/Great-tailed_grackle'
        input_args = ['main.py',_url, _url]

        assert_that(calling(main.get_nodes).with_args(spider_stub,true_url_validator_stub,input_args),raises(ValueError))

    def test_invalid_url_throws_value_error(self):
        ''' Tests that we only accept well formed URLS'''
        _url = 'https://en.wikipedia.org/wiki/Great-tailed_grackle'
        input_args = ['main.py', _url]

        assert_that(calling(main.get_nodes).with_args(spider_stub,false_url_validator_stub,input_args),raises(ValueError))


    def test_is_valid_url_validates_wiki_returns_true(self):
        ''' Test that our wikipedia links are valid'''
        _url = 'http://en.wikipedia.org/wiki/Great-tailed_grackle'
        out = main.is_valid_url(_url)
        assert_that(out,equal_to(True))


    def test_is_valid_url_validates_invalid_url_returns_true(self):
        ''' Demonstrate that this validator is pretty weak'''
        _url = 'http://en.wikipedia.org/wiki/anything_and:stuff#lots;of*invalid0Stuff'
        out = main.is_valid_url(_url)
        assert_that(out,equal_to(True))

    def test_is_valid_url_validates_invalid_url_returns_true(self):
        ''' Validate that it denies basic non wiki URLS'''
        _url = 'google.com'
        out = main.is_valid_url(_url)
        assert_that(out,equal_to(False))
