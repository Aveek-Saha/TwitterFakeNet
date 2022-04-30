import sys
import csv
import os
import json
import datetime
import time

from tqdm import tqdm

from utils import *

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

for data_choice in data_collection_choice:
    with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
                                    data_choice["label"]), encoding="UTF-8") as csvfile:
        lines = len(csvfile.readlines())

    with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
                                    data_choice["label"]), encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        dump_dir = "{}/tweets".format(dump_location)

        print("Collecting {} {}".format(data_choice["news_source"], data_choice["label"]))
        for news in tqdm(reader, total=lines):
            tweets =  [int(tweet_id) for tweet_id in news["tweet_ids"].split("\t") if tweet_id.isdigit() if not os.path.exists("{}/{}.json".format(dump_dir, tweet_id))]
            total_tweets += tweets

print(len(total_tweets))
print(len(list(set(total_tweets))))

unique_tweet_ids = list(set(total_tweets))

dump_dir = "{}/tweets".format(dump_location)
create_dir(dump_dir)

dump_dir_rt = "{}/retweets".format(dump_location)
create_dir(dump_dir_rt)

keys_file = "keys.json"
keys = json.load(open(keys_file, 'r'))

apis = []
for key in keys:
    api = create_api(key)
    apis.append({"connection": api, "available": 1, "time": None})

n = 100
groups = [unique_tweet_ids[i:i+n] for i in range(0, len(unique_tweet_ids), n)]

for group in tqdm(groups):
    try:
        tweets = get_tweets(apis, ",".join(map(str, group)))
        for tweet in tweets:
            json.dump(tweet, open(
                "{}/{}.json".format(dump_dir, tweet["id_str"]), "w"))
    except Exception as e:
        print("Error: ", e)

