import sys
import csv
import os
import json
from tqdm import tqdm

dataset_path = "../FakeNewsNet/dataset"
dump_location = "fakenewsnet_dataset"

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


for data_choice in data_collection_choice:
    load_news_file(data_choice)