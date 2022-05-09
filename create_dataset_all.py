import sys
import csv
import os
import json
from unicodedata import category

from tqdm import tqdm

from utils import *

# userid_dict = {line.strip(): {"politifact_fake": [], "politifact_real": [
# ], "gossipcop_fake": [], "gossipcop_real": []} for line in lines}


def new_user():
    return {"politifact_fake": [], "politifact_real": [], "gossipcop_fake": [], "gossipcop_real": [], 
    "politifact_fake_rt": [], "politifact_real_rt": [], "gossipcop_fake_rt": [], "gossipcop_real_rt": [], }


maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)

users = {}


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
                if (tweet_id.isdigit() and os.path.exists("{}/{}.json".format(dump_dir, tweet_id))):
                    tweet = json.load(
                        open("{}/{}.json".format(dump_dir, tweet_id), 'r'))
                    user_id = tweet["user"]["id_str"]
                    if user_id not in users:
                        users[user_id] = new_user()
                    
                    data_category = "{}_{}".format(data_choice["news_source"], data_choice["label"])
                    users[user_id][data_category].append(tweet_id)

                if (tweet_id.isdigit() and os.path.exists("{}/{}.json".format(dump_dir_rt, tweet_id))):
                    retweets = json.load(open("{}/{}.json".format(dump_dir_rt, tweet_id), "r"))
                    for retweet in retweets:
                        try:
                            user_id = retweet["user"]["id_str"]
                            if user_id not in users:
                                users[user_id] = new_user()
                            data_category = "{}_{}_rt".format(data_choice["news_source"], data_choice["label"])
                            users[user_id][data_category].append(tweet_id)
                        except Exception as e:
                            print(retweet)

for userid in users:
    users[userid]["total_count"] = 0
    for data_choice in data_collection_choice:
        data_category = "{}_{}".format(data_choice["news_source"], data_choice["label"])
        data_category_rt = "{}_{}_rt".format(data_choice["news_source"], data_choice["label"])
        users[userid][data_category + "_count"] = len(users[userid][data_category])
        users[userid]["total_count"] += len(users[userid][data_category])
        users[userid][data_category_rt + "_count"] = len(users[userid][data_category_rt])
        users[userid]["total_count"] += len(users[userid][data_category_rt])

json.dump(users, open(
                "{}/user_map_all.json".format(dump_location), "w"), indent=4)

with open('{}/all.txt'.format(dump_location), 'w', encoding='utf-8') as f:
    f.write(str.join('\n', (str(x) for x in users.keys())))