# Twitter Fake News Network

An exploration of the users responsible for the circulation of fake news Twitter. Specifically looking into how likely is it that an article shared by an user is fake.

## How to run

### 1. Collect tweets and retweets

Run the scripts for tweet and retweet collection

```
python collect_tweets.py
python collect_retweets.py
```

### 2. Compile a list of users

Run the next script to create a list of user ids from the collected tweets and retweets

```
python create_dataset.py
```

### 3. Collect user information

Use tweego to collect information about the users from their ids

### 4. Filter dataset

Filter the dataset to include only users that:

1. Have shared more than 2 new articles
1. Follow less than or equal to 5000 other users
1. Have at least 5000 followers

```
python filter_dataset.py
```

The reason behind these constraints is:

1. We want users who've shared at least a couple of articles to establish a pattern
1. Users who have followed more than 5k users have done so most likely with a bot
1. Anyone with more than 5k followers is bound to contribute to news spreading among a large community

### 5. Create user network

Use the tweego tool to construct the user network and store it as a .gml file

### 6. Add features to graph

Add features to the nodes like, the number of news articles, if a user is verified or not, and the amount of fake news shared as a fraction of the total news

```
python edit_graph.py
```

### 7. Classification

Run the classification scripts in any order

-   GNN
-   node2vec

Purpose of each notebook-

-   **GNN -** Use different Graph Neural Networks to classify fake and real users
-   **node2vec -** Use node2vec combined with different ML models to classify fake and real users

## Background

## Dataset

To build a classification model that would find patterns in ego networks to detect users that share predominantly fake news, a dataset containing edges between users and a database of tweets and retweets that have been manually classified as real or fake is required. Such a dataset does not exist already, but it can be generated.

### 1. Tweego

### 2. FakeNewsNet

[FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet) is a fake news data repository, which contains two comprehensive datasets that includes news content, social context, and dynamic information. The full paper can be found [here](https://arxiv.org/pdf/1809.01286.pdf). The news is obtained from _two_ fact-checking websites to obtain news with ground truth labels for fake news and true news, these websites are-

-   #### PolitiFact
    In PolitiFact, journalists and domain experts review the political news and provide fact-checking evaluation results to claim news articles as fake or real.
-   #### GossipCop
    GossipCop is a website for fact-checking entertainment stories aggregated from various media outlets. GossipCop provides rating scores on the scale of 0 to 10 to classify a news story as the degree from fake to real.

The most important feature of FakeNewsNet is that it also downloads tweets and retweets sharing the news articles from Twitter. This means that we can get the profile of users that shared the tweets from Twitter, and then combine it with our list of verified users to see how many fake/real news articles every verified user shared.

### Stats

**Sample size of users:** 9687

|        | Friends |  Followers  |  Listed   |  Statuses  | Articles shared | Fake ratio |
| :----: | :-----: | :---------: | :-------: | :--------: | :-------------: | :--------: |
|  mean  | 1648.99 |  257043.19  |  1299.34  | 137100.58  |      17.11      |    0.42    |
| median | 1189.00 |  17216.00   |  256.00   |  72894.00  |      5.00       |    0.33    |
|  min   |  0.00   |   5000.00   |   0.00    |   139.00   |      3.00       |    0.0     |
|  max   | 5000.00 | 72123733.00 | 215288.00 | 8318206.00 |    55768.00     |    1.00    |

## Creating Labels

To create the labels, the ratio of fake news shared to total number of articles shared is considered. The FakeNewsNet dataset contains real and fake news for both Politifact and GossipCop. So first the total number of fake/real news articles a user has shared is calculated by checking how many times their display name or id matches the id or display name of the user sharing a tweet. From this we can get the total number of fake and real news articles a user has shared from both sources(Politifact and GossipCop) and then find the ratio of fake to total news shared.

If more than half the news articles a user has tweeted are fake, then that user is assigned a label of 1, and if less than half are fake, they are given a label of 0. So a label of 1 means the account shares mostly fake news, and a label of 0 means the news shared is mostly real.

<!-- ## Creating Features

Apart from the number of friends, followers, lists and statuses, we need some more meaningful features for classification. There is no point in adding any manually engineered graph features since the graph neural networks and node2vec algorithms used for classification will automatically determine the best features to use during training.

So instead features generated from the text from both user bio descriptions and tweets will be used. The features we'll be generating are from-

1. ### Sentiment analysis
    Using the [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) library, we can get the average polarity and subjectivity of their profile description and all tweets they have made
2. ### Empath
    [Empath](https://github.com/Ejhfast/empath-client) is a tool for analyzing text across lexical categories. The idea here is that some topics may be more likely to generate fake news, and users whose tweets frequently contain these topics may be more likely to share fake news.
    The empath tool analyzes text and counts words that fall into around 200 predefined categories like envy, family, crime, masculine, health, dispute and many more. -->

## Edgelist

Using nucoll it is possible to generate a GML file of a users first and second degree relationships on Twitter. In order to generate the graph, nucoll retrieves the handle's friends (or followers) and all friends-of-friends (2nd degree relationships). It then looks for friend relationships among the friends/followers of the handle.

In this case the handle we supply to nucoll is @verified, and a file with all the 1st and 2nd degree relationships of users that are friends of @verified is generated.

Because of Twitter's very restrictive API rate limits, generating the edge list of all 330k+ verified users is not feasible, so the users are filtered. The following restrictions were applied-

1. The user must have shared at least one real, and one fake article
2. The user must be following less than 10k people. The reason for this is, it's highly unlikely that a user with more than 10000 friends manually followed so many accounts and they probably used bots.

When these constraints are applied, around 3000 users are left. The edge list for these users is stored in a `.gml` file, which can be imported to create a networkx graph.

## Classification

Two different approaches are taken to build a classification model.

1. ### Node2vec

    Node2vec learns continuous representations for nodes in a graph. The implementation of node2vec used can be found [here](https://github.com/eliorc/node2vec).

    After combining node2vec with the node features, the classifiers trained are-

    - **Random forest**
    - **SVM**
    - **Logistic regression**
    - **XGBoost**

2. ### Graph neural networks
    GNNs directly operate on the graph structure
    - **GraphSAGE -** Learns the embedding for each node in an inductive way. Each node is represented by the aggregation of its neighborhood. Thus, even if a new node unseen during training time appears in the graph, it can still be properly represented by its neighboring nodes.
    - **Graph Convolutional Networks -** A neural network, designed to work on graphs

## Analysis

### Baseline

For a baseline, the performance of classifiers on just the sentiment and empath features without any network information is taken.

|               | Accuracy | Precision | Recall | f1 Score |
| :-----------: | :------: | :-------: | :----: | :------: |
|  Naive Bayes  |  0.659   |   0.660   | 0.660  |  0.660   |
|      KNN      |  0.628   |   0.680   | 0.630  |  0.600   |
| Logistic Reg  |  0.686   |   0.690   | 0.690  |  0.680   |
|      SVM      |  0.716   |   0.720   | 0.720  |  0.720   |
|    XGBoost    |  0.710   |   0.710   | 0.710  |  0.710   |
| Random Forest |  0.662   |   0.660   | 0.660  |  0.660   |

### GNNs

|           | Accuracy | Precision | Recall | f1 Score |
| :-------: | :------: | :-------: | :----: | :------: |
| GraphSage |  0.730   |   0.710   | 0.850  |  0.773   |
|    GCN    |  0.671   |   0.654   | 0.827  |  0.709   |
|    GAT    |  0.541   |   0.543   | 0.987  |  0.650   |

### Node2vec

|               | Accuracy | Precision | Recall | f1 Score |
| :-----------: | :------: | :-------: | :----: | :------: |
|  Naive Bayes  |  0.610   |   0.630   | 0.620  |  0.610   |
|      KNN      |  0.671   |   0.670   | 0.670  |  0.670   |
| Logistic Reg  |  0.678   |   0.680   | 0.680  |  0.670   |
|      SVM      |  0.728   |   0.730   | 0.730  |  0.720   |
|    XGBoost    |  0.728   |   0.730   | 0.730  |  0.720   |
| Random Forest |  0.659   |   0.670   | 0.660  |  0.660   |

### Learnt embeddings

The classifiers are trained on the embeddings learnt by the GraphSAGE and GCN models

-   **GraphSAGE**

    |               | Accuracy | Precision | Recall | f1 Score |
    | :-----------: | :------: | :-------: | :----: | :------: |
    |  Naive Bayes  |  0.724   |   0.720   | 0.720  |  0.720   |
    |      KNN      |  0.691   |   0.690   | 0.690  |  0.690   |
    | Logistic Reg  |  0.700   |   0.700   | 0.700  |  0.700   |
    |      SVM      |  0.719   |   0.730   | 0.720  |  0.710   |
    |    XGBoost    |  0.713   |   0.720   | 0.710  |  0.710   |
    | Random Forest |  0.679   |   0.680   | 0.680  |  0.680   |

-   **GCN**

    |               | Accuracy | Precision | Recall | f1 Score |
    | :-----------: | :------: | :-------: | :----: | :------: |
    |  Naive Bayes  |  0.702   |   0.700   | 0.700  |  0.700   |
    |      KNN      |  0.621   |   0.670   | 0.620  |  0.520   |
    | Logistic Reg  |  0.716   |   0.730   | 0.720  |  0.710   |
    |      SVM      |  0.725   |   0.740   | 0.730  |  0.720   |
    |    XGBoost    |  0.729   |   0.730   | 0.730  |  0.730   |
    | Random Forest |  0.695   |   0.690   | 0.690  |  0.690   |

-   **GAT**

    |               | Accuracy | Precision | Recall | f1 Score |
    | :-----------: | :------: | :-------: | :----: | :------: |
    |  Naive Bayes  |  0.662   |   0.670   | 0.660  |  0.660   |
    |      KNN      |  0.646   |   0.670   | 0.650  |  0.530   |
    | Logistic Reg  |  0.717   |   0.730   | 0.720  |  0.710   |
    |      SVM      |  0.719   |   0.740   | 0.720  |  0.710   |
    |    XGBoost    |  0.724   |   0.730   | 0.720  |  0.720   |
    | Random Forest |  0.595   |   0.600   | 0.600  |  0.090   |

## Results

**Accuracy**

|           | Naive Bayes |  KNN  | Logistic Reg |  SVM  | XGBoost | Random Forest |
| :-------: | :---------: | :---: | :----------: | :---: | :-----: | :-----------: |
| Baseline  |    0.659    | 0.628 |    0.686     | 0.716 |  0.710  |     0.662     |
| GraphSAGE |    0.724    | 0.691 |    0.700     | 0.719 |  0.713  |     0.679     |
|    GCN    |    0.702    | 0.621 |    0.716     | 0.725 |  0.729  |     0.695     |
| Node2vec  |    0.610    | 0.671 |    0.678     | 0.728 |  0.728  |     0.659     |
|    GAT    |    0.662    | 0.646 |    0.717     | 0.719 |  0.724  |     0.595     |

From the table above, it is evident that for classifying users as fake news sources, the structure of the network helps increase the accuracy of classification

## Citing

If you use this repository in your research please cite

```
@misc{Saha_TwitterFakeNet_2020,
	author = {Saha, Aveek},
	month = {3},
	title = {{TwitterFakeNet}},
	url = {https://github.com/Aveek-Saha/TwitterFakeNet},
	year = {2020}
}
```
