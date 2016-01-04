import json
import os
import requests
import webbrowser

from get_twitter_api_params import get_rate_limit_rules, save_api_dict
from lxml import html
from twython import Twython


#-- APP CREDENTIALS -------------------------------->>>
filepath = "{}/.twitter_credentials".format(os.path.expanduser('~'))
with open(filepath, "r") as cred_file:
    APP_KEY, APP_SECRET = cred_file.read().splitlines()
#--------------------------------------------------->>>


class TweetCatcher():
    def __init__(self):
        app_creds = Twython(APP_KEY, APP_SECRET).get_authentication_tokens()
        self.client = self.gen_client()
        self.get_api_dict()


    def gen_client(self):
        filepath = "{}/.tweetcatcher_oath".format(os.path.expanduser('~'))
        if os.path.isfile(filepath):
            with open(filepath, "r") as oauth_file:
                oauth_tokens = oauth_file.read().splitlines()
            return Twython( app_key=APP_KEY, 
                            app_secret=APP_SECRET, 
                            oauth_token=oauth_tokens[0], 
                            oauth_token_secret=oauth_tokens[1] )
        else:
            webbrowser.open(app_creds['auth_url'])

            pin = raw_input('Enter PIN: ')
            
            oauth = Twython( app_key=APP_KEY, 
                             app_secret=APP_SECRET, 
                             oauth_token=app_creds['oauth_token'], 
                             oauth_token_secret=app_creds['oauth_token_secret'] ).get_authorized_tokens(pin)

            return Twython( app_key=APP_KEY, 
                            app_secret=APP_SECRET, 
                            oauth_token=oauth['oauth_token'], 
                            oauth_token_secret=oauth['oauth_token_secret'] )

    def catch(self, endpoint):
        if endpoint in self.twitter_endpoints['GET']:
            new_params = self.interact('GET', endpoint)
            return self.client.get(endpoint, new_params)
        elif endpoint in self.twitter_endpoints['POST']:
            new_params = self.interact('POST', endpoint)
            return self.client.post(endpoint, new_params)
        else:
            print("\n*** Please use an actual endpoint. See TweetCatcher.twitter_endpoints for details ***\n")

    def save_oauth_tokens(self):
        filepath = "{}/.tweetcatcher_oath".format(os.path.expanduser('~'))
        with open(filepath, "w") as oauth_file:
            oauth_file.write("{}\n{}\n".format(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET))

    def get_api_dict(self):
        try:
            filepath = "{}/.twitter_api".format(os.path.expanduser('~'))
            with open(filepath, "r") as api_file:
                api_dict = json.load(api_file)
            self.twitter_endpoints = api_dict
        except IOError as e:
            self.twitter_endpoints = save_api_dict()

    def interact(self, method, endpoint):
        params = self.twitter_endpoints[method][endpoint]
        print('-'*20)
        print('Please enter values for the following params: ')
        print('-'*20)
        for param in params.iterkeys():
            params[param] = raw_input('{} = '.format(param)) or None
        return params
            
