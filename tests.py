# import requests
import get_twitter_api_params
import unittest

from get_twitter_api_params import *
from mock import MagicMock, patch


def mocked_response(url, **response_dict):
    class Response(type):
        def __str__(self):
            return "<{} [valid_url? {}, has_content? {}]>".format(self.__name__, 
                                                                  'http://' in args[0], 
                                                                  'content' in self.__dict__)
    if 'http://' in url:
        response_dict.update({'status_code': 200,
                           'content': '[insert content here...]'})
        return type.__new__(Response, "Response", (), response_dict)
    else: 
        response_dict.update({'status_code': 404,
                           'errors': '***INVALID URL***'})
        return type.__new__(Response, "Response", (), response_dict)        


class TestGetTwitterAPIParams(unittest.TestCase):

    @patch('get_twitter_api_params.requests.get', side_effect=mocked_response)
    def test_get_page_root(self, mock_get):
        html_str = '''<!DOCTYPE html>
                    <html>
                    <head>
                        <title>My First HTML Page</title>
                    </head>
                    <body>
                        My text goes here.
                    </body>
                    </html>'''
        mock_response_dict = {'content': html_str,
                              'api': {'GET': [], 'POST': []}}

        print ">" * 20
        print mocked_response('200', **mock_response_dict)
        print mocked_response('200', **mock_response_dict).errors
        print mocked_response(url='http://google.com', **mock_response_dict)
        # print get_twitter_api_params.requests.get(mock_response_dict)
        print ">" * 20
        print "mock_get", mock_get
        # print "mock_get.__dict__", mock_get.__dict__
        print "mock_get._mock_side_effect", mock_get._mock_side_effect('http://google.com')
        print "get_page_root", get_page_root('https://dev.twitter.com/rest/public')
        # mock_get.get.return_value = mocked_response

        assert 0

        
    # fetch_params
        # get_page_root
    # get_all_public_rest_endpoints
    # build_api_dict
    # build_all_endpoint_ref_urls
    # get_all_api_params
    # get_rate_limit_rules


if __name__ == "__main__":
    unittest.main()