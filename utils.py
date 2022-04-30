import os
import datetime
import time

from TwitterAPI import TwitterAPI

dataset_path = "../FakeNewsNet/dataset"
dump_location = "../fakenewsnet_dataset"

data_collection_choice = [
    {
      "news_source": "politifact",
      "label": "fake"
    },
    {
      "news_source": "politifact",
      "label": "real"
    },
    {
      "news_source": "gossipcop",
      "label": "fake"
    },
    {
      "news_source": "gossipcop",
      "label": "real"
    }
]

def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def create_api(config):
    # Create a Twitter API object
    api = TwitterAPI(config['app_key'],
                     config['app_secret'],
                     config['oauth_token'],
                     config['oauth_token_secret']
                     )
    return api


def pick_api(apis):
    # Pick an API object that hasn't timed out
    available = [api["available"] for api in apis]
    if all(v == 0 for v in available):
        return None, -1
    for index, api in enumerate(apis):
        if api["available"] == 1:
            return api, index


def api_request(apis, endpoint, params):
    # Send a request using an available API object
    api, index = pick_api(apis)
    if index != -1:
        r = api["connection"].request(endpoint, params)
        if r.headers['x-rate-limit-remaining'] == '0':
            apis[index]["available"] = 0
            return (api_request(apis, endpoint, params))
        return(r)

    else:
        apis[index]["available"] = 0
        wait_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
        print('\nHit the API limit. Waiting for refresh at {}.'
              .format(wait_time.strftime("%H:%M:%S")))
        time.sleep(15 * 60)
        for api in apis:
            api["available"] = 1
        return (api_request(apis, endpoint, params))

def get_tweets(apis, tweet_id):

    r = api_request(apis,
                    'statuses/lookup', {'id': tweet_id, "trim_user": "true", 'include_entities': "false"})

    tweets = r.json()

    if 'errors' in r.json():
        if r.json()['errors'][0]['code'] == 34:
            return(tweets)

    return(tweets)

def create_api_app_auth(config):
    # Create a Twitter API object
    api = TwitterAPI(config['app_key'],
                     config['app_secret'],
                     auth_type='oAuth2'
                     )
    return api


def get_retweets(apis, tweet_id):

    r = api_request(apis,
                    'statuses/retweets/:%s' % tweet_id, {"trim_user": "true"})

    tweets = r.json()

    if 'errors' in r.json():
        if r.json()['errors'][0]['code'] == 34:
            return(tweets)

    return(tweets)