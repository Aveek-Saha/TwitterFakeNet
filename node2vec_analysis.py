import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from node2vec import Node2Vec


from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing, feature_extraction
from sklearn.model_selection import train_test_split
# from sklearn import metrics
from sklearn.manifold import TSNE

from sklearn.metrics import accuracy_score, f1_score, classification_report, mean_squared_error
from sklearn.metrics import precision_score, recall_score, confusion_matrix
# from sklearn.model_selection import GridSearchCV
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.decomposition import TruncatedSVD
# from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV
import warnings
# import xgboost as xgb
warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans

# from stellargraph.data import BiasedRandomWalk
# from stellargraph import StellarGraph

# from gensim.models import Word2Vec

from utils import *

screen_name = "verified"

graph = nx.read_gml("{}/{}_features.gml".format(dump_location, screen_name))

# G = StellarGraph.from_networkx(graph)

# print(G.info())

# rw = BiasedRandomWalk(G)

# walks = rw.run(
#     nodes=list(G.nodes()),  # root nodes
#     length=40,  # maximum length of a random walk
#     n=300,  # number of random walks per root node
#     p=0.5,  # Defines (unormalised) probability, 1/p, of returning to source node
#     q=3.0,  # Defines (unormalised) probability, 1/q, for moving away from source node
# )
# print("Number of random walks: {}".format(len(walks)))

# str_walks = [[str(n) for n in walk] for walk in walks]
# model = Word2Vec(str_walks, vector_size=128, window=5, min_count=0, sg=1, workers=4, epochs=1)

# # Retrieve node embeddings and corresponding subjects
# node_ids = model.wv.index_to_key  # list of node IDs
# node_embeddings = (
#     model.wv.vectors
# )  # numpy.ndarray of size number of nodes times embeddings dimensionality
# # node_targets = node_subjects[[int(node_id) for node_id in node_ids]]

# tsne = TSNE(n_components=2)
# node_embeddings_2d = tsne.fit_transform(node_embeddings)

# alpha = 0.7
# # label_map = {l: i for i, l in enumerate(np.unique(node_targets))}
# node_targets = [ 1 if node[1]["fake"] >= 0.3 else 0 for node in list(graph.nodes(data=True))]
# # node_targets = [node[1]["fake"] for node in list(graph.nodes(data=True))]
# # node_colours = ['red' if l == 1 else 'blue' for l in target]

# # plt.figure(figsize=(10, 8))
# # plt.scatter(
# #     node_embeddings_2d[:, 0],
# #     node_embeddings_2d[:, 1],
# #     c=node_colours,
# #     cmap="jet",
# #     alpha=alpha,
# # )

# # plt.show()

# # X will hold the 128-dimensional input features
# X = node_embeddings
# # y holds the corresponding target values
# y = np.array(node_targets)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# clf = LogisticRegressionCV(cv=5,  
#                           max_iter=10000)
# clf.fit(X_train, y_train)
# y_pred = clf.predict_proba(X_test)

# y_pred_class = ((y_pred[:, 1]>=0.3)*1).flatten()

# print(classification_report(y_test, y_pred_class))
# print(accuracy_score(y_test, y_pred_class))


node2vec = Node2Vec(graph, dimensions=128, walk_length=40, num_walks=300, workers=1, p=.5, q=3)

vmodel = node2vec.fit()

node_ids = vmodel.wv.index_to_key  # list of node IDs
node_embeddings = (
    vmodel.wv.vectors
)  # numpy.ndarray of size number of nodes times embeddings dimensionality
# node_targets = node_subjects[[int(node_id) for node_id in node_ids]]

tsne = TSNE(n_components=2)
node_embeddings_2d = tsne.fit_transform(node_embeddings)

alpha = 0.7

node_targets = [ 1 if node[1]["fake"] >= 0.5 else 0 for node in list(graph.nodes(data=True))]
node_colours = ['red' if l == 1 else 'green' for l in node_targets]

plt.figure(figsize=(10, 8))
plt.scatter(
    node_embeddings_2d[:, 0],
    node_embeddings_2d[:, 1],
    c=node_colours,
    cmap="jet",
    alpha=alpha,
)

plt.show()