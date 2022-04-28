import math
import sys
import csv
import os
import json
import datetime
import time

from tqdm import tqdm

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


def load_news_file(data_choice):
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
                                    data_choice["label"]), encoding="UTF-8") as csvfile:
        lines = len(csvfile.readlines())

    with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
                                    data_choice["label"]), encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)

        print("Collecting {} {}".format(data_choice["news_source"], data_choice["label"]))
        for news in tqdm(reader, total=lines):
            # news_list.append(news, data_choice["label"], data_choice["news_source"])
            try:
                tweets =  [int(tweet_id) for tweet_id in news["tweet_ids"].split("\t")]
                for tweet in tqdm(tweets):
                    dump_dir = "{}/{}/{}/{}".format(dump_location, data_choice["news_source"], data_choice["label"], news["id"])
                    tweet_dir = "{}/tweets".format(dump_dir)
                    create_dir(dump_dir)
                    create_dir(tweet_dir)

                    tweet_file = "{}/{}.json".format(tweet_dir, tweet)

                    if os.path.exists(tweet_file):
                        continue

                    os.system("snscrape --jsonl twitter-tweet {} > {}/{}.json".format(tweet, tweet_dir, tweet))

            except Exception as e:
                print("Error: ", e)
                pass


# for data_choice in data_collection_choice:
#     load_news_file(data_choice)

def create_api(config):
    # Create a Twitter API object
    api = TwitterAPI(config['app_key'],
                     config['app_secret'],
                     config['oauth_token'],
                     config['oauth_token_secret']
                     )
    return api

def create_api_app_auth(config):
    # Create a Twitter API object
    api = TwitterAPI(config['app_key'],
                     config['app_secret'],
                     auth_type='oAuth2'
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

total_tweets = []

maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)

# for data_choice in data_collection_choice:
#     with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
#                                     data_choice["label"]), encoding="UTF-8") as csvfile:
#         lines = len(csvfile.readlines())

#     with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
#                                     data_choice["label"]), encoding="UTF-8") as csvfile:
#         reader = csv.DictReader(csvfile)
#         dump_dir = "{}/tweets".format(dump_location)

#         print("Collecting {} {}".format(data_choice["news_source"], data_choice["label"]))
#         for news in tqdm(reader, total=lines):
#             tweets =  [int(tweet_id) for tweet_id in news["tweet_ids"].split("\t") if tweet_id.isdigit() if os.path.exists("{}/{}.json".format(dump_dir, tweet_id))]
#             # tweets =  [int(tweet_id) for tweet_id in news["tweet_ids"].split("\t") if tweet_id.isdigit() if not os.path.exists("{}/{}.json".format(dump_dir, tweet_id))]
#             total_tweets += tweets

# print(len(total_tweets))
# print(len(list(set(total_tweets))))

# unique_tweet_ids = list(set(total_tweets))

dump_dir = "{}/tweets".format(dump_location)
create_dir(dump_dir)

dump_dir_rt = "{}/retweets".format(dump_location)
create_dir(dump_dir_rt)

keys_file = "keys.json"
keys = json.load(open(keys_file, 'r'))

apis = []
for key in keys:
    # api = create_api(key)
    api = create_api_app_auth(key)
    apis.append({"connection": api, "available": 1, "time": None})

# n = 100
# groups = [unique_tweet_ids[i:i+n] for i in range(0, len(unique_tweet_ids), n)]

# for group in tqdm(groups):
#     try:
#         tweets = get_tweets(apis, ",".join(map(str, group)))
#         for tweet in tweets:
#             json.dump(tweet, open(
#                 "{}/{}.json".format(dump_dir, tweet["id_str"]), "w"))
#     except Exception as e:
#         print("Error: ", e)

# retweet_counts = []
# retweet_counts_non_zero = []

# retweet_map = {}

# for tweet_id in tqdm(unique_tweet_ids):
#     tweet = json.load(open("{}/{}.json".format(dump_dir, tweet_id), 'r'))
#     retweet_count = tweet["retweet_count"]
#     retweet_map[str(tweet_id)] = tweet["retweet_count"]
#     retweet_counts.append(retweet_count)
#     if retweet_count > 0:
#         retweet_counts_non_zero.append(retweet_count)

# json.dump(retweet_map, open(
#                 "{}/retweet_map.json".format(dump_location), "w"))

retweet_map = json.load(open("{}/retweet_map.json".format(dump_location), 'r'))

for tweet_id in retweet_map:
    if (retweet_map[tweet_id] > 0):
