import json
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils import *

users_location = "../dataset_tweego/users"
screen_name = "all_10k"

# graph = nx.read_gml("{}/{}_features.gml".format(dump_location, screen_name))
# graph_nodes = list(graph.nodes(data=True))

# data = []
# for index, node in enumerate(tqdm(graph_nodes)):
#     user_id = node[1]["userid"]
#     label = node[0]
#     user_data = []
#     if os.path.exists("{}/{}.json".format(users_location, str(user_id))):
#         user = json.load(open("{}/{}.json".format(users_location, str(user_id)), "r"))
#         user_data.append(user["id_str"])
#         user_data.append(user["screen_name"])
#         user_data.append(node[1]["verified"])
#         user_data.append(user["friends_count"])
#         user_data.append(user["followers_count"])
#         user_data.append(user["listed_count"])
#         user_data.append(user["statuses_count"])
#         user_data.append(node[1]["total_count"])
#         user_data.append(node[1]["fake"])
#         user_data.append(node[1]["political"])
#         user_data.append(user["created_at"])
#         user_data.append(user["location"])

#     data.append(user_data)


# df = pd.DataFrame(data, columns=["userId", "ScreenName", "Verified", "FriendsCount", "FollowersCount", "ListedCount", "StatusesCount", "NewsCount", "Fake", "Political", "CreatedAt", "Location"])

# df.to_csv('{}/{}_features.csv'.format(dump_location, screen_name), index=False)

df = pd.read_csv('{}/{}_features.csv'.format(dump_location, screen_name))

pd.options.display.float_format = '{:.2f}'.format

# print(df[['FriendsCount', 'FollowersCount', 'ListedCount', 'StatusesCount', 'NewsCount', 'Fake']].describe())

# fig = plt.figure(figsize=(15,5))
# ax = fig.gca()

# fol_max = 1000000
# df[df['FollowersCount'] < fol_max].hist(column='FollowersCount', bins=200)
# plt.xticks(np.arange(0, fol_max+1, fol_max/10))

# plt.ylabel("Number of users", fontsize=12)
# plt.xlabel("Number of followers",fontsize=12)

# plt.show()

# fr_max = 5000
# df[df['FriendsCount'] < fr_max].hist(column='FriendsCount', bins=50, ax=ax)
# plt.xticks(np.arange(0, fr_max+1, fr_max/10))

# plt.ylabel("Number of users", fontsize=12)
# plt.xlabel("Number of friends",fontsize=12)

# plt.show()

# status_max = 100000
# df[df['StatusesCount'] < status_max].hist(column='StatusesCount', bins=200, ax=ax)
# plt.xticks(np.arange(0, status_max+1, status_max/10))

# plt.ylabel("Number of users", fontsize=12)
# plt.xlabel("Number of satuses",fontsize=12)

# plt.show()

# news_max = 1000
# df[df['NewsCount'] < news_max].hist(column='StatusesCount', bins=200, ax=ax)
# plt.xticks(np.arange(0, news_max+1, news_max/10))

# plt.ylabel("Number of users", fontsize=12)
# plt.xlabel("Number of news articles",fontsize=12)

# plt.show()

# df["Location"].value_counts()[:50].plot.bar(figsize=(20,7))

# plt.xlabel("Location", fontsize=13)
# plt.ylabel("Number of users",fontsize=13)

# plt.show()

# dates = list(df['CreatedAt'].values)

# created = []

# for date in dates:
#     created.append(date.split()[-1])

# df['year'] = created

# df['year'].groupby(df["year"]).count().plot(kind = 'bar', figsize=(15,5))

# plt.xlabel("Year", fontsize=13)
# plt.ylabel("Number of users",fontsize=13)

# plt.show()

# df["Political"].value_counts().plot.bar()
# plt.show()

# df["Verified"].value_counts().plot.bar()
# plt.show()

# df["Political"].value_counts().plot.bar()
# plt.show()

df['Fake_bin'] = [1 if x >= 0.5 else 0 for x in df['Fake']]

# df.hist(column='Fake', bins=20)
# plt.show()

df["Fake_bin"].value_counts().plot.bar()
plt.show()