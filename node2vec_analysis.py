import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from node2vec import Node2Vec


from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing, feature_extraction
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE

from sklearn.metrics import accuracy_score, f1_score, classification_report, mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV
import warnings
import xgboost as xgb
warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans

from utils import *

screen_name = "all_10k"
threshhold = 0.5

graph = nx.read_gml("{}/{}_features.gml".format(dump_location, screen_name))

node2vec = Node2Vec(graph, dimensions=128, walk_length=40, num_walks=300, workers=1, p=.5, q=3)

vmodel = node2vec.fit()

node_ids = vmodel.wv.index_to_key  # list of node IDs
vectors = vmodel.wv.vectors

graph_nodes = list(graph.nodes(data=True))

X_feat = []

node_targets = []
for index, id in enumerate(node_ids):
    result = next((v for v in graph_nodes if v[0] == id), None)
    fake = result[1]["fake"]
    vector = list(vectors[index])
    feats = [result[1]["followers_count"], result[1]["friends_count"], result[1]["listed_count"], result[1]["statuses_count"], result[1]["verified"], result[1]["political"]]
    X_feat.append(vector + feats)
    if fake >= threshhold:
        node_targets.append(1)
    else:
        node_targets.append(0)

node_embeddings = (
    X_feat
)


# tsne = TSNE(n_components=2)
# node_embeddings_2d = tsne.fit_transform(node_embeddings)

# alpha = 0.7
# node_colours = ['red' if l == 1 else 'green' for l in node_targets]
# plt.figure(figsize=(10, 8))
# plt.scatter(
#     node_embeddings_2d[:, 0],
#     node_embeddings_2d[:, 1],
#     c=node_colours,
#     cmap="jet",
#     alpha=alpha,
# )

# plt.show()

X = node_embeddings
y = np.array(node_targets)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

scaler = StandardScaler()
scaled_X_train = scaler.fit_transform(X_train)
scaled_X_test = scaler.transform(X_test)


print("\n Logistic Regession: ")
clf = LogisticRegressionCV(Cs=10, cv=10, max_iter=300)
clf.fit(scaled_X_train, y_train)
y_pred = clf.predict(scaled_X_test)

print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


print("\n Naive Bayes: ")
gnb = GaussianNB()
gnb.fit(scaled_X_train, y_train)

y_pred = gnb.predict(scaled_X_test)

print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


print("\n SVM: ")
clf = svm.SVC(kernel='rbf', gamma='scale')
clf.fit(scaled_X_train, y_train)

y_pred = clf.predict(scaled_X_test)

print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


print("\n K Nearest Neighbors: ")
knn = KNeighborsClassifier(n_neighbors=10)
knn.fit(scaled_X_train, y_train)

y_pred = knn.predict(scaled_X_test)

print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


print("\n Random Forest: ")
forest = RandomForestClassifier()
forest.fit(scaled_X_train, y_train)
y_pred = forest.predict(scaled_X_test)

print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))


print("\n XGBoost: ")
xgb_clf = xgb.XGBClassifier()
xgb_clf.fit(scaled_X_train, y_train)
y_pred = xgb_clf.predict(scaled_X_test)

print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))