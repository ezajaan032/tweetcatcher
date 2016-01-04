import json
import os
import requests
import sys

from lxml import html


def save_api_dict():
    api_dict_with_params = get_all_api_params()
    filepath = "{}/.twitter_api".format(os.path.expanduser('~'))
    with open(filepath, "w") as api_file:
        json.dump(api_dict_with_params, api_file)
    return api_dict_with_params

#################################################

def fetch_params(endpoint_ref_url):
    param_elements = get_page_root(endpoint_ref_url).xpath('//div[@class="Field-items"]/div/div/span')
    param_keys = [ param.text for param in param_elements ]
    return { key.strip():None for key in param_keys }

def get_page_root(url):
    response = requests.get(url)
    page = response.content
    return html.fromstring(page)

def get_all_public_rest_endpoints(api_ref_url='https://dev.twitter.com/rest/public'):
    page_root = get_page_root(api_ref_url)
    menu_elements = page_root.xpath('//ul[@class="menu"]/li')
    return [ option.text_content() for option in menu_elements 
             if ('GET' in option.text_content() or 
                 'POST' in option.text_content()) ][1:]

def build_api_dict(api_ref_url='https://dev.twitter.com/rest/public'):
    api_dict = { 'GET': {}, 'POST': {} }
    endpoints = get_all_public_rest_endpoints()
    split_endpoints = [ str.split(endpoint, ' ') for endpoint in endpoints ]
    for endpoint in split_endpoints:
        if endpoint[0] == 'GET':
            api_dict['GET'][endpoint[1]] = None
        elif endpoint[0] == 'POST':
            api_dict['POST'][endpoint[1]] = None
    return api_dict

def build_all_endpoint_ref_urls(api_dict):
    url_base = 'https://dev.twitter.com/rest/reference/'
    endpoint_paths = [ 'get/' + path for path in  api_dict['GET'].keys() ] + [ 'post/' + path for path in api_dict['POST'].keys() ]
    endpoint_urls = []
    for endpoint in endpoint_paths:
        endpoint_urls.append(url_base + endpoint)
    return endpoint_urls

def get_all_api_params():
    url_base = 'https://dev.twitter.com/rest/reference/'
    api_dict = build_api_dict()
    endpoint_urls = build_all_endpoint_ref_urls(api_dict)

    print('\n*** Please wait. Fetching API endpoints from https://dev.twitter.com/rest/reference/ ***\n')
    print('    --> this could take a while...\n')
    for url in endpoint_urls:
        sys.stdout.write('.')
        if '/get/' in url:
            get_endpoint = url.replace(url_base+'get/', '')
            api_dict['GET'][get_endpoint] = fetch_params(url)
        elif '/post/' in url:
            post_endpoint = url.replace(url_base+'post/', '')
            api_dict['POST'][post_endpoint] = fetch_params(url)
    print('\n')

    return api_dict

def get_rate_limit_rules():
    trl_response = requests.get('https://dev.twitter.com/rest/public/rate-limits')
    trl = trl_response.content
    trl_page = html.fromstring(trl)
    trl_table_header = trl_page.xpath('//table/thead/tr/th')
    trl_table_body = trl_page.xpath('//table/tbody')[0].getchildren()

    rate_limit_headers = ['endpoint', 'resource_type', 'app_limit', 'user_limit']
    rate_limit_rules = [ zip(rate_limit_headers, [cell.text_content().strip() for cell in row.xpath('td')]) for row in trl_table_body ]
    rate_limits = { str.split(rule[0][1], ' ')[-1]:{k:v for k,v in rule[1:]} for rule in rate_limit_rules }
    return rate_limits
