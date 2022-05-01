import sys
import csv
import os
import json
from unicodedata import category

from tqdm import tqdm

from utils import *


# with open("{}/verified.txt".format(dump_location)) as fp:
#     lines = fp.readlines()

# userid_dict = {line.strip(): {"politifact_fake": [], "politifact_real": [
# ], "gossipcop_fake": [], "gossipcop_real": []} for line in lines}

# total_tweets = []

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

#         print("Collecting {} {}".format(
#             data_choice["news_source"], data_choice["label"]))
#         for news in tqdm(reader, total=lines):
#             # tweets = [int(tweet_id) for tweet_id in news["tweet_ids"].split(
#             #     "\t") if tweet_id.isdigit() if os.path.exists("{}/{}.json".format(dump_dir, tweet_id))]
#             # total_tweets += tweets
#             for tweet_id in news["tweet_ids"].split("\t"):
#                 if (tweet_id.isdigit() and os.path.exists("{}/{}.json".format(dump_dir, tweet_id))):
#                     tweet = json.load(open("{}/{}.json".format(dump_dir, tweet_id), 'r'))
#                     user_id = tweet["user"]["id_str"]
#                     if user_id in userid_dict:
#                         data_category = "{}_{}".format(data_choice["news_source"], data_choice["label"])
#                         userid_dict[user_id][data_category].append(tweet_id)

# user_dict_present = {}

# for userid in userid_dict:
#     userid_dict[userid]["total_count"] = 0
#     for data_choice in data_collection_choice:
#         data_category = "{}_{}".format(data_choice["news_source"], data_choice["label"])
#         userid_dict[userid][data_category + "_count"] = len(userid_dict[userid][data_category])
#         userid_dict[userid]["total_count"] += len(userid_dict[userid][data_category])
#         # userid_dict[userid][data_category] = "\t".join(userid_dict[userid][data_category])
#     if userid_dict[userid]["total_count"] > 0:
#         user_dict_present[userid] = userid_dict[userid]
        

# json.dump(user_dict_present, open(
#                 "{}/user_map.json".format(dump_location), "w"), indent=4)

user_dict_present = json.load(open("{}/user_map.json".format(dump_location), 'r'))
# print(len({ user: user_dict_present[user] for user in user_dict_present if user_dict_present[user]["total_count"] > 3}))

for user in user_dict_present:
    user_dict_present[user]["politifact_fake_rt"] = []
    user_dict_present[user]["politifact_real_rt"] = []
    user_dict_present[user]["gossipcop_fake_rt"] = []
    user_dict_present[user]["gossipcop_real_rt"] = []

retweet_map = json.load(open("{}/retweet_map.json".format(dump_location), 'r'))
retweet_map_filtered = dict(filter(lambda e:e[1]>0, retweet_map.items()))

for data_choice in data_collection_choice:
    with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
                                    data_choice["label"]), encoding="UTF-8") as csvfile:
        lines = len(csvfile.readlines())

    with open('{}/{}_{}.csv'.format(dataset_path, data_choice["news_source"],
                                    data_choice["label"]), encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        dump_dir = "{}/tweets".format(dump_location)
        dump_dir_rt = "{}/retweets".format(dump_location)

        print("Collecting {} {}".format(
            data_choice["news_source"], data_choice["label"]))
        for news in tqdm(reader, total=lines):
            for tweet_id in news["tweet_ids"].split("\t"):
                if (tweet_id.isdigit() and os.path.exists("{}/{}.json".format(dump_dir_rt, tweet_id))):
                    retweets = json.load(open("{}/{}.json".format(dump_dir_rt, tweet_id), "r"))
                    for retweet in retweets:
                        try:
                            user_id = retweet["user"]["id_str"]
                            if user_id in user_dict_present:
                                data_category = "{}_{}_rt".format(data_choice["news_source"], data_choice["label"])
                                user_dict_present[user_id][data_category].append(tweet_id)
                        except Exception as e:
                            print(retweet)


for userid in user_dict_present:
    for data_choice in data_collection_choice:
        data_category = "{}_{}_rt".format(data_choice["news_source"], data_choice["label"])
        user_dict_present[userid][data_category + "_count"] = len(user_dict_present[userid][data_category])
        user_dict_present[userid]["total_count"] += len(user_dict_present[userid][data_category])

json.dump(user_dict_present, open(
                "{}/user_map_rt.json".format(dump_location), "w"), indent=4)