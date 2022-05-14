import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import isnan

import stellargraph as sg
from stellargraph.mapper import GraphSAGENodeGenerator, FullBatchNodeGenerator, DirectedGraphSAGENodeGenerator
from stellargraph.layer import GraphSAGE, GCN, GAT, DirectedGraphSAGE
from stellargraph import globalvar

from tensorflow.keras import layers, optimizers, losses, metrics, Model
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing, feature_extraction
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import classification_report
from keras.callbacks import EarlyStopping

from utils import *
screen_name = "all_10k"

graph = nx.read_gml("{}/{}_features.gml".format(dump_location, screen_name))
graph_nodes = list(graph.nodes(data=True))

X_feat = []

node_targets = []
for node in graph_nodes:
    result = node
    fake = result[1]["fake"]
    feats = [result[1]["followers_count"], result[1]["friends_count"], result[1]["listed_count"], result[1]["statuses_count"], result[1]["verified"], result[1]["political"]]
    X_feat.append(feats)
    if fake >= 0.3:
        node_targets.append(1)
    else:
        node_targets.append(0)


X = X_feat
y = np.array(node_targets)

df = pd.DataFrame.from_dict(dict(graph.nodes(data=True)), orient='index')
user_features = df.drop(columns=['fake', 'userid', 'total_count'])

X_train, X_test, y_train, y_test = train_test_split(user_features, y, test_size=0.3)

scaler = StandardScaler()
scaled_X_train = scaler.fit_transform(X_train)
scaled_X_test = scaler.transform(X_test)

df[['followers_count', 'friends_count', 'listed_count', 'verified', 'statuses_count', 'political']] = scaler.fit_transform(user_features.values)

train_targets= y_train.reshape((-1,1))
test_targets= y_test.reshape((-1,1))


stg = sg.StellarGraph.from_networkx(graph, node_features=user_features)
# stg = sg.StellarGraph.from_networkx(graph)

model_type = 'graphsage'    # Can be either gcn, gat, or graphsage


if model_type == "graphsage":
    # For GraphSAGE model
    batch_size = 100; 
    in_samples = [20, 4]
    out_samples = [10, 2]
    epochs = 300
    
    generator = DirectedGraphSAGENodeGenerator(stg, batch_size, in_samples, out_samples)
    train_gen = generator.flow(X_train.index, 
                               train_targets, 
                               shuffle=True)
    
    base_model = DirectedGraphSAGE(
        layer_sizes=[32, 32],
        generator=generator,
        bias=False,
        dropout=0.5,
    )
    x_inp, x_out = base_model.in_out_tensors()
    prediction = layers.Dense(units=1, activation="sigmoid")(x_out)
    
elif model_type == "gcn":
    # For GCN model
    epochs = 100 
    
    generator = FullBatchNodeGenerator(stg, method="gcn", sparse=True)
    train_gen = generator.flow(X_train.index, 
                               train_targets, )
    
    base_model = GCN(
        layer_sizes=[16, 16],
        generator = generator,
        bias=True,
        dropout=0.5,
        activations=["relu", "relu"]
    )
    x_inp, x_out = base_model.in_out_tensors()
    prediction = layers.Dense(units=1, activation="sigmoid")(x_out)
    
elif model_type == "gat":
    # For GAT model
    layer_sizes = [8, 1]
    attention_heads = 8
    epochs = 100
    
    generator = FullBatchNodeGenerator(stg, method="gat", sparse=True)
    train_gen = generator.flow(X_train.index, 
                               train_targets,)
    
    base_model = GAT(
        layer_sizes=layer_sizes,
        attn_heads=attention_heads,
        generator=generator,
        bias=True,
        in_dropout=0.5,
        attn_dropout=0.5,
        activations=["relu", "sigmoid"],
        normalize=None,
    )
    x_inp, prediction = base_model.node_model()

model = Model(inputs=x_inp, outputs=prediction)

model.compile(
    optimizer=optimizers.Adam(lr=0.005),
    loss=losses.binary_crossentropy,
    metrics=["acc"],
)

test_gen = generator.flow(X_test.index, test_targets)

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,  patience=30)

history = model.fit(
    train_gen,
    epochs=epochs,
    validation_data=test_gen,
    verbose=2,
    callbacks=[es],
    shuffle=False,
)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')

plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')

plt.show()

test_metrics = model.evaluate(test_gen)
print("\nTest Set Metrics:")
for name, val in zip(model.metrics_names, test_metrics):
    print("\t{}: {:0.4f}".format(name, val))