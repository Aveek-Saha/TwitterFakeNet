import sys
import csv
import os
import json

from tqdm import tqdm

from utils import *

users_location = "../dataset_tweego/users"

# friends = []
# with open('{}/all.txt'.format(dump_location)) as f:
#     for line in f:
#         friends.append(str(line).strip())

user_dict = json.load(open("{}/user_map_all.json".format(dump_location)))

friends = user_dict.keys()

filtered_friends = {}

for friend in tqdm(friends):
    if user_dict[friend]["total_count"] > 2:
        if os.path.exists("{}/{}.json".format(users_location, str(friend))):
            user = json.load(open("{}/{}.json".format(users_location, str(friend)), "r"))
            if user["followers_count"] >= 5000 and user["friends_count"] <= 5000:
                filtered_friends[friend] = {}
                filtered_friends[friend]["followers_count"] = user["followers_count"]
                filtered_friends[friend]["total_count"] = user_dict[friend]["total_count"]

print(len(filtered_friends.keys()))

with open('{}/all_filtered.txt'.format(dump_location), 'w', encoding='utf-8') as f:
    f.write(str.join('\n', (str(x) for x in filtered_friends.keys())))

json.dump(filtered_friends, open(
                "{}/user_map_all_filtered.json".format(dump_location), "w"), indent=4)