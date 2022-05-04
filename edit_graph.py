import json
import networkx as nx

from tqdm import tqdm
from utils import *

screen_name = "verified"

G = nx.read_gml("{}/{}.gml".format(dump_location, screen_name))

G.remove_node(screen_name)
# print(len(list(nx.isolates(G))))

G.remove_node("suggestonline")
G.remove_node("PolitiFact")
G.remove_node("PolitiFactTexas")
G.remove_nodes_from(list(nx.isolates(G)))


nodes = list(G.nodes(data=True))

user_dict_present = json.load(open("{}/user_map_rt.json".format(dump_location), 'r'))
user_dict_filtered = { user: user_dict_present[user] for user in user_dict_present if user_dict_present[user]["total_count"] > 2}

details = {}

for index, node in enumerate(tqdm(nodes)):
    user = node[1]["userid"]
    label = node[0]
    fake = user_dict_filtered[user]["politifact_fake_count"] + user_dict_filtered[user]["gossipcop_fake_count"] + user_dict_filtered[user]["politifact_fake_rt_count"] + user_dict_filtered[user]["gossipcop_fake_rt_count"]
    real = user_dict_filtered[user]["politifact_real_count"] + user_dict_filtered[user]["gossipcop_real_count"] + user_dict_filtered[user]["politifact_real_rt_count"] + user_dict_filtered[user]["gossipcop_real_rt_count"]

    pol = user_dict_filtered[user]["politifact_fake_count"] + user_dict_filtered[user]["politifact_fake_rt_count"] + user_dict_filtered[user]["politifact_real_count"] + user_dict_filtered[user]["politifact_real_rt_count"]
    gos = user_dict_filtered[user]["gossipcop_fake_count"] + user_dict_filtered[user]["gossipcop_fake_rt_count"] + user_dict_filtered[user]["gossipcop_real_count"] + user_dict_filtered[user]["gossipcop_real_rt_count"]

    details[label] = {}
    details[label]["total_count"] = user_dict_filtered[user]["total_count"]

    ratio = fake/(fake + real)
    details[label]["fake"] = ratio

    if gos > pol:
        details[label]["political"] = 0
    else:
        details[label]["political"] = 1

nx.set_node_attributes(G, details)


nx.write_gml(G, "{}/{}_features.gml".format(dump_location, screen_name))
