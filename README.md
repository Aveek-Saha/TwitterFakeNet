# Twitter Fake News Network
An exploration of Twitter's Verified users and the news articles they tweet. Specifically looking into how likely is it that an article shared by the user is fake.

## Background
### What is a verified user?
Every user that is verified is given a blue badge and this lets people know that an account of public interest is authentic.

According to Twitter-
> An account may be verified if it is determined to be an account of public interest. Typically this includes accounts maintained by users in music, acting, fashion, government, politics, religion, journalism, media, sports, business, and other key interest areas. A verified badge does not imply an endorsement by Twitter.

So accounts are generally verified if they belong to public figures, like politicians, comedians, businessmen, etc or organizations like news networks, sports teams, corporations and so on.


### Why verified users?
The verified status does not make the account any more credible than it was before verification and from this recent paper, [Does Being Verified Make You More Credible?](https://security.cs.georgetown.edu/~tavish/twitter-credibility-chi2019.pdf) we can see that most users understand this.

Because of the nature of accounts that get the verified status, they generally have a large following, average: 117k, median: 10k. So they're crucial in the dissemination and propagation of information. This is why it's worthwhile exploring how reliable or trustworthy these users are as news sources.

### How to tell if a user is verified?
When you go to a users profile, if they have a small blue/white icon next to their username with a tick, that looks something like this <img src="https://github.com/Aveek-Saha/TwitterFakeNet/blob/master/figures/verified.png" width="20" title="verified icon">, then that user is verified but there is no obvious way to write a script to collect details of all such users.

There is an official Twitter Verified account, [@verified](https://twitter.com/verified), and if you look closely at all the accounts it follows, it's easy to see it follows every verified account on Twitter. A few people might have blocked @verified but we can assume that the number is small and can be ignored. 

I picked up this method and some ideas for analysis from an article by [Luca Hammer](https://medium.com/startup-grind/analyzing-205-718-verified-twitter-users-cf0811781ac8).


## Dataset
To build a classification model that would find patterns in ego networks to detect verified users that share predominantly fake news, a dataset containing edges between users and a database of tweets and retweets that have been manually classified as real or fake is required. Such a dataset does not exist already, but it can be generated.

### 1. Twecoll
[Twecoll](https://github.com/jdevoo/twecoll) is a command line tool used to retrieve data from Twitter. Using twecoll, we can generate a list of all users that a user follows, and then generate a follower graph from this data.

Once `twecoll` is done getting the list of users that @verified follows, it generates a `<username>.dat` file containing information about every user in that list. The important information downloaded is-
- User ID- an unique identifier for the user
- Name- the display name of the user
- Friends, Followers, Listed, Statuses count- number of: friends, followers a user has, lists a user is included in, statuses(tweets) a user has made
- Date created- the date the account was created
- Location- where the user is located, this location is self reported, and Twitter has no autocomplete for this location, so spelling mistakes are common and the data isnt very reliable

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


### Final dataset



## Classification


