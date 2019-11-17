# Twitter Fake News Network
An exploration of Twitter's Verified users and the news articles they tweet. Specifically looking into how likely is it that an article shared by the user is fake.

## How to run

This repository is meant to be cloned inside `FakeNewsNet/code`.

Purpose of each notebook-
* **user_data -** Collect all the user tweets, retweets, descriptions collected from FakeNewsNet and count the number of fake and real news articles
* **extract_features -** Create the features for all 300k+ verified users 
* **user_analysis -** Some basic analysis on the verified accounts
* **GNN -** Use different Graph Neural Networks to classify fake and real users
* **node2vec -** Use node2vec combined with different ML models to classify fake and real users

1. Get FakeNewsNet
2. Clone this repository in the `FakeNewsNet/code` folder
3. For a new list of verified users run the `twecoll` tool, copy the `verified.dat` file to the datasets folder
4. Run the Jupyter Notebooks in the following order
	* user_data
	* extract_features
	* user_analysis(optional)
5. Rename `datasets/verified_3k.dat` to `verified.dat` and replace the file in the `twecoll` folder
6. Run the twecoll fetch command
7. Run the edgelist command and put the resulting `verified.gml` file in the `datasets` folder
8. Run the classification files in any order
	* GNN
	* node2vec


## Background
### What is a verified user?
Every user that is verified is given a blue/white badge and this lets people know that an account of public interest is authentic.

According to Twitter-
> An account may be verified if it is determined to be an account of public interest. Typically this includes accounts maintained by users in music, acting, fashion, government, politics, religion, journalism, media, sports, business, and other key interest areas. A verified badge does not imply an endorsement by Twitter.

So accounts are generally verified if they belong to public figures, like politicians, comedians, businessmen, etc or organizations like news networks, sports teams, corporations and so on.


### Why verified users?
The verified status does not make the account any more credible than it was before verification and from this recent paper, [Does Being Verified Make You More Credible?](https://security.cs.georgetown.edu/~tavish/twitter-credibility-chi2019.pdf) we can see that most users understand this.

Because of the nature of accounts that get the verified status, they generally have a large following, average: 117k, median: 10k. So they're crucial in the dissemination and propagation of information. This is why it's worthwhile exploring how reliable or trustworthy these users are as news sources.

### How to tell if a user is verified?
When you go to a users profile, if they have a small blue/white icon next to their username with a tick, that looks like this <img src="https://github.com/Aveek-Saha/TwitterFakeNet/blob/master/figures/verified.png" width="20" title="verified icon">, then that user is verified but there is no obvious way to write a script to collect details of all such users.

There is an official Twitter Verified account [@verified](https://twitter.com/verified), and if you look closely at all the accounts it follows, it's easy to see it follows every verified account on Twitter. A few people might have blocked @verified but we can assume that the number is small and can be ignored. 

I picked up this method and some ideas for analysis from an article by [Luca Hammer](https://medium.com/startup-grind/analyzing-205-718-verified-twitter-users-cf0811781ac8).


## Dataset
To build a classification model that would find patterns in ego networks to detect verified users that share predominantly fake news, a dataset containing edges between users and a database of tweets and retweets that have been manually classified as real or fake is required. Such a dataset does not exist already, but it can be generated.

### 1. Twecoll
[Twecoll](https://github.com/jdevoo/twecoll) is a command line tool used to retrieve data from Twitter. Using twecoll, we can generate a list of all users that a user follows, and then generate a follower graph from this data.

Once `twecoll` is done getting the list of users that @verified follows, it generates a `<username>.dat` file containing information about every user in that list. The important information downloaded is-
- User ID- a unique identifier for the user
- Name- the display name of the user
- Friends, Followers, Listed, Statuses count- number of: friends, followers a user has, lists a user is included in, statuses(tweets) a user has made
- Date created- the date the account was created
- Location- where the user is located, this location is self reported, and Twitter has no autocomplete for this location, so spelling mistakes are common and the data is not very reliable

### 2. FakeNewsNet
[FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet) is a fake news data repository, which contains two comprehensive datasets that includes news content, social context, and dynamic information. The full paper can be found [here](https://arxiv.org/pdf/1809.01286.pdf). The news is obtained from *two* fact-checking websites to obtain news with ground truth labels for fake news and true news, these websites are-

- #### PolitiFact
	 In PolitiFact, journalists and domain experts review the political news and provide fact-checking evaluation results to claim news articles as fake or real.
- #### GossipCop
	 GossipCop is a website for fact-checking entertainment stories aggregated from various media outlets. GossipCop provides rating scores on the
scale of 0 to 10 to classify a news story as the degree from fake to real.

The most important feature of FakeNewsNet is that it also downloads tweets and retweets sharing the news articles from Twitter. This means that we can get the profile of users that shared the tweets from Twitter, and then combine it with our list of verified users to see how many fake/real news articles every verified user shared.


### Stats

**Total number of verified users as of Oct 2019:** 335018
 

|        | Friends    | Followers    | Listed     | Statuses    |
|--------|------------|--------------|------------|-------------|
| mean   | 2074.95    | 116570.99    | 510.01     | 16671.92    |
| median | 532.00     | 10152.00     | 122.00     | 5366.00     |
| min    | 0.0        | 0.0          | 0.0        | 0.0         |
| max    | 4494592.00 | 108831215.00 | 3177668.00 | 50437226.00 |


## Creating Labels

To create the labels, the ratio of fake news shared to total number of articles shared is considered. The FakeNewsNet dataset contains real and fake news for both Politifact and GossipCop. So first the total number of fake/real news articles a user has shared is calculated by checking how many times their display name or id matches the id or display name of the user sharing a tweet. From this we can get the total number of fake and real news articles a user has shared from both sources(Politifact and GossipCop) and then find the ratio of fake to total news shared.

If more than half the news articles a user has tweeted are fake, then that user is assigned a label of 1, and if less than half are fake, they are given a label of 0. So a label of 1 means the account shares mostly fake news, and a label of 0 means the news shared is mostly real.

## Creating Features

Apart from the number of friends, followers, lists and statuses, we need some more meaningful features for classification. There is no point in adding any manually engineered graph features since the graph neural networks and node2vec algorithms used for classification will automatically determine the best features to use during training.

So instead features generated from the text from both user bio descriptions and tweets will be used. The features we'll be generating are from-

1. ### Sentiment analysis
	 Using the [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) library, we can get the average polarity and subjectivity of their profile description and all tweets they have made 
	 
2. ### Empath
	 [Empath](https://github.com/Ejhfast/empath-client) is a tool for analyzing text across lexical categories. The idea here is that some topics may be more likely to generate fake news, and users whose tweets frequently contain these topics may be more likely to share fake news.
	 
	 The empath tool analyzes text and counts words that fall into around 200 predefined categories like envy, family, crime, masculine, health, dispute and many more.
	 
## Edgelist
Using twecoll it is possible to generate a GML file of a users first and second degree relationships on Twitter. In order to generate the graph, twecoll retrieves the handle's friends (or followers) and all friends-of-friends (2nd degree relationships). It then looks for friend relationships among the friends/followers of the handle.

In this case the handle we supply to twecoll is @verified, and a file with all the 1st and 2nd degree relationships of users that are friends of @verified is generated.

Because of Twitter's very restrictive API rate limits, generating the edge list of all 330k+ verified users is not feasible, so the users are filtered. The following restrictions were applied-

1. The user must have shared at least one real, and one fake article
2. The user must be following less than 10k people. The reason for this is, it's highly unlikely that a user with more than 10000 friends manually followed so many accounts and they probably used bots.

When these constraints are applied, around 3000 users are left. The edge list for these users is stored in a `.gml` file, which can be imported to create a networkx graph.

## Classification
Two different approaches are taken to build a classification model.

1. ### Node2vec
	 Node2vec learns continuous representations for nodes in a graph. The implementation of node2vec used can be found [here](https://github.com/eliorc/node2vec). 
	 
	 After combining node2vec with the node features, the classifiers trained are-
	 * **Random forest**
	 * **SVM**
	 * **Logistic regression**
	 * **XGBoost**

2. ### Graph neural networks
	GNNs directly operate on the graph structure
	* **GraphSAGE -** Learns the embedding for each node in an inductive way. Each node is represented by the aggregation of its neighborhood. Thus, even if a new node unseen during training time appears in the graph, it can still be properly represented by its neighboring nodes.
	* **Graph Convolutional Networks -** A neural network, designed to work on graphs


## Analysis

### Baseline
For a baseline, the performance of classifiers on just the sentiment and empath features without any network information is taken.

|               | Accuracy | Precision | Recall | f1 Score |
|:-------------:|:--------:|:---------:|:------:|:--------:|
|      SVM      |   71.55  |   72.00   |  72.00 |   71.00  |
|    XGBoost    |   71.03  |   71.00   |  71.00 |   71.00  |
| Random Forest |   68.79  |   69.00   |  69.00 |   69.00  |
|  Logistic Reg |   68.62  |   69.00   |  69.00 |   68.00  |


### GNNs

|           | Accuracy | Precision | Recall | f1 Score |
|:---------:|:--------:|:---------:|:------:|:--------:|
| GraphSage |   73.10  |   74.00   |  73.00 |   73.00  |
|    GCN    |   68.96  |   70.00   |  69.00 |   68.00  |



### Node2vec

|               | Accuracy | Precision | Recall | f1 Score |
|:-------------:|:--------:|:---------:|:------:|:--------:|
|      SVM      |   00.00  |   00.00   |  00.00 |   00.00  |
|  Logistic Reg |   00.00  |   00.00   |  00.00 |   00.00  |
| Random Forest |   00.00  |   00.00   |  00.00 |   00.00  |
|    XGBoost    |   00.00  |   00.00   |  00.00 |   00.00  |



### Learnt embeddings
The classifiers are trained on the embeddings learnt by the GraphSAGE and GCN models
**GraphSAGE**

|               | Accuracy | Precision | Recall | f1 Score |
|:-------------:|:--------:|:---------:|:------:|:--------:|
|      SVM      |   72.06  |   73.00   |  72.00 |   72.00  |
|  Logistic Reg |   71.03  |   71.00   |  71.00 |   71.00  |
| Random Forest |   68.79  |   69.00   |  69.00 |   69.00  |
|    XGBoost    |   69.82  |   70.00   |  70.00 |   70.00  |

**GCN**

|               | Accuracy | Precision | Recall | f1 Score |
|:-------------:|:--------:|:---------:|:------:|:--------:|
|      SVM      |   71.89  |   73.00   |  72.00 |   72.00  |
|  Logistic Reg |   71.03  |   72.00   |  71.00 |   71.00  |
| Random Forest |   73.44  |   74.00   |  73.00 |   73.00  |
|    XGBoost    |   73.10  |   74.00   |  73.00 |   73.00  |













