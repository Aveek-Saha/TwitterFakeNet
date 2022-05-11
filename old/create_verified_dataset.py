import json
import os
import glob
import pprint
from tqdm import tqdm
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/verified.dat")

ids = list(df['#ID'])

users = {}

for i in ids:
    users[i] = {
        'uid': i,
        'pf_fake': 0,
        'pf_real': 0,
        'gc_fake': 0,
        'gc_real': 0,
        'description': '',
        'tweets': []
    }

dataset_path = "../FakeNewsNet/code/fakenewsnet_dataset"

def update_user_dict(data, user_dict, source, label):
    col = {
        "politifact_fake": 'pf_fake',
        "politifact_real": 'pf_real',
        "gossipcop_fake": 'gc_fake',
        "gossipcop_real": 'gc_real'
    }

    tweet = data['text']
    des = data['user']['description']
    user_id = data['user']['id']
    
    if user_id in user_dict:
        user_dict[user_id][col["{}_{}".format(source, label)]]+=1
        user_dict[user_id]['description'] = des
        user_dict[user_id]['tweets'].append(tweet)

    return user_dict

def get_data(user_dict, dataset_path, source, label, tweet_type):

    files = glob.iglob("/{}/{}/*/{}/*.json".format(dataset_path, source, label, tweet_type))

    for file in tqdm(files):
        with open(file, encoding='utf-8', mode='r') as currentFile:
            data = json.load(currentFile)
            if tweet_type == "retweets":
                for d in data['retweets']:
                    user_dict = update_user_dict(d, user_dict, source, label)
            elif tweet_type == "tweets":
                user_dict = update_user_dict(data, user_dict)
                
    return user_dict


user_dict = users
user_dict = get_data(user_dict, dataset_path, "politifact", "fake", "tweets")
user_dict = get_data(user_dict, dataset_path, "politifact", "fake", "retweets")
user_dict = get_data(user_dict, dataset_path, "politifact", "real", "tweets")
user_dict = get_data(user_dict, dataset_path, "politifact", "real", "retweets")
user_dict = get_data(user_dict, dataset_path, "gossipcop", "fake", "tweets")
user_dict = get_data(user_dict, dataset_path, "gossipcop", "fake", "retweets")
user_dict = get_data(user_dict, dataset_path, "gossipcop", "real", "tweets")
user_dict = get_data(user_dict, dataset_path, "gossipcop", "real", "retweets")

list_of_lists = []

for user_id in user_dict:
    gc_fake = user_dict[user_id]['gc_fake']
    gc_real = user_dict[user_id]['gc_real']
    pf_fake = user_dict[user_id]['pf_fake']
    pf_real = user_dict[user_id]['pf_real']
    des = user_dict[user_id]['description']
    tweets = "^".join(user_dict[user_id]['tweets'])
    
    list_of_lists.append([user_id, pf_fake, pf_real, gc_fake, gc_real, des, tweets])

df_tw = pd.DataFrame(list_of_lists, columns=["uid", 'pf_fake','pf_real','gc_fake','gc_real', 'description', 'tweets'])
df.drop(['Protected', 'CreatedAt', 'URL', 'ProfileImageURL', 'Location', 'Subject', 'Relation', 'Verified'], axis=1, inplace=True)

df_feat = df.merge(df_tw, how='inner', left_on='#ID', right_on='uid')

df_feat['total_fake'] = df_feat['pf_fake'] + df_feat['gc_fake']
df_feat['total_real'] = df_feat['pf_real'] + df_feat['gc_real']

df_feat['net_trust'] = df_feat['total_real'] - df_feat['total_fake']

df_feat['total_news'] = df_feat['total_real'] + df_feat['total_fake']
df_feat['fake_prob'] = df_feat['total_fake'] / df_feat['total_news']

df_feat['net_trust_norm'] = df_feat['net_trust']/df_feat['total_news']

df_feat['fake'] = [1 if x >= 0.5 else 0 if x < 0.5 else 2 for x in df_feat['fake_prob']]

df_final = df_feat[
     (df_feat['ScreenName'] != 'GossipCop') & (df_feat['ScreenName'] != 'PolitiFact')
#      & (df_feat['net_trust_norm'] != 0)
     & (df_feat['FriendsCount'] <= 10000)
     & (df_feat['total_fake'] > 0)
     & (df_feat['total_real'] > 0)
    ].sort_values(['total_news', 'net_trust_norm', 'net_trust', 'FollowersCount'], ascending=False)

df_final['fake'] = [1 if x >= 0.5 else 0 if x < 0.5 else 2 for x in df_final['fake_prob']]

df_final.to_csv('datasets/verified_features_3k.csv', index=False)

dat = pd.read_csv("datasets/verified.dat")
filtered = dat[dat['#ID'].isin(list(df_final['#ID']))]

filtered.to_csv('datasets/verified_3k.dat', index = False)