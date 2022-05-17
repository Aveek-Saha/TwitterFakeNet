import json
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils import *

users_location = "../dataset_tweego/users"
screen_name = "all_10k"

graph = nx.read_gml("{}/{}_features.gml".format(dump_location, screen_name))
graph_nodes = list(graph.nodes(data=True))

data = []
for index, node in enumerate(tqdm(graph_nodes)):
    user_id = node[1]["userid"]
    label = node[0]
    user_data = []
    if os.path.exists("{}/{}.json".format(users_location, str(user_id))):
        user = json.load(open("{}/{}.json".format(users_location, str(user_id)), "r"))
        user_data.append(user["id_str"])
        user_data.append(user["screen_name"])
        user_data.append(node[1]["verified"])
        user_data.append(user["friends_count"])
        user_data.append(user["followers_count"])
        user_data.append(user["listed_count"])
        user_data.append(user["statuses_count"])
        user_data.append(node[1]["total_count"])
        user_data.append(node[1]["fake"])
        user_data.append(node[1]["political"])
        user_data.append(user["created_at"])
        user_data.append(user["location"])

    data.append(user_data)


df = pd.DataFrame(data, columns=["userId", "ScreenName", "Verified", "FriendsCount", "FollowersCount", "ListedCount", "StatusesCount", "NewsCount", "Fake", "Political", "CreatedAt", "Location"])

df.to_csv('{}/{}_features.csv'.format(dump_location, screen_name), index=False)