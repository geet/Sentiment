from __future__ import division
from collections import defaultdict

class NaiveBayesClassifier:
        # Initialize the index.
        # The index is a 2-D array implemented using nested dictionaries
        index = defaultdict(lambda: defaultdict(int))
        # Two categories in which tweets are to be classified,
        # positive and negative
        categories = ["pos", "neg"]
        # Initial token count for each category
        categoryTokenCounts = {"pos":0, "neg":0}
        tokenCount = 0
        categoryTweetCounts = {"pos":0, "neg":0}
        tweetCount = 0
        prior = {"pos":0.5, "neg":0.5}
        def classify(self,tokens,category_counts,tweet_counts,token_counts):
                self.categoryTweetCounts["pos"]=tweet_counts[0]
                self.categoryTweetCounts["neg"]=tweet_counts[1]
                self.tweetCount=tweet_counts[0]+tweet_counts[1]
                self.categoryTokenCounts["pos"]=token_counts[0]
                self.categoryTokenCounts["neg"]=token_counts[1]
                self.tokenCount=token_counts[0]+token_counts[1]
                #Set the prior probability, which is assumed to be 0.5 for each category
                self.prior["pos"] = self.categoryTweetCounts["pos"]/self.tweetCount
                self.prior["neg"] = self.categoryTweetCounts["neg"]/self.tweetCount
                #print tokens
                categoryScores = {"pos":1, "neg":1}
                print tokens	
                #print self.index	
                for category in self.categories:
                        for token in tokens:
                                categoryScores[category] *= (category_counts[token][category] + 1)/(self.categoryTokenCounts[category] + self.tokenCount)
                        categoryScores[category] = self.prior[category] * categoryScores[category]
                return max(categoryScores, key =categoryScores.get)
