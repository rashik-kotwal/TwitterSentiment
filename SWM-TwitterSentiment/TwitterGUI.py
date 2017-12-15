import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

from tkinter import *
from tkinter import ttk, filedialog, messagebox



class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'JKq0QqRiTaZ3GdwBpWnmBTV4Q'
        consumer_secret = 'QSXK5XMHcssjZkM8BvrBGryluc6GAu1GW7F47wo072qWVE9I81'
        access_token = '793888526-zOZVdw2l1P6bRxvU8NyoMKm7B3PeVcPMDpmTuwx3'
        access_token_secret = 'k9EhcXRND12ItaXFYBV40WS4PwEYdP1soGpTrqCVWWHba'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))



def main(val):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    global tweets
    tweets = api.get_tweets(query=val, count=200)

    # picking positive tweets from tweets
    global ptweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    global ntweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

    # percentage of neutral tweets

    print("Neutral tweets percentage: {} % ".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

def sentiment(val):
    if(val==''):
        messagebox.showerror("Error","Enter Keyword!!")
        return
    main(val)


    answerStringA = 100 * len(ntweets) / len(tweets)
    before_dec, after_dec = str(answerStringA).split('.')
    tempA=float('.'.join((before_dec, after_dec[0:2])))
    answerStringA=tempA
    answerStringA=str(answerStringA)+'%'
    Negative_tweets_percentage_ans = ttk.Label(root, text=answerStringA, font="bold").grid(column=2, row=3, sticky='e')

    answerStringB = 100 * len(ptweets) / len(tweets)
    before_dec, after_dec = str(answerStringB).split('.')
    tempB = float('.'.join((before_dec, after_dec[0:2])))
    answerStringB=tempB
    answerStringB = str(answerStringB) + "%"
    Positive_tweets_percentage_ans = ttk.Label(root, text=answerStringB, font="bold").grid(column=2, row=4, sticky='e')

    answerStringC = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)
    before_dec, after_dec = str(answerStringC).split('.')
    tempC = float('.'.join((before_dec, after_dec[0:2])))
    answerStringC=tempC
    answerStringC = str(answerStringC) + "%"
    Neutral_tweets_percentage_ans = ttk.Label(root, text=answerStringC, font="bold").grid(column=2, row=5, sticky='e')

    return

if __name__ == "__main__":
    # calling main function
    root = Tk()

    root.wm_title("Twitter Sentiment Analysis")

    root.wm_geometry("700x300")
    EnterQuery = ttk.Label(root, text='Enter keyword:   ', font="bold").grid(column=1, row=2, sticky='e')

    Negative_tweets_percentage = ttk.Label(root, text='Negative tweets percentage    ', font="bold").grid(column=1,
                                                                                                           row=3,
                                                                                                           sticky='e',columnspan=1)
    Positive_tweets_percentage = ttk.Label(root, text='Positive tweets percentage    ', font="bold").grid(column=1,
                                                                                                           row=4,
                                                                                                           sticky='e',columnspan=1)
    Neutral_tweets_percentage = ttk.Label(root, text='Neutral tweets percentage    ', font="bold").grid(column=1,
                                                                                                         row=5,
                                                                                                         sticky='e',columnspan=1)
    e1 = Entry(root)
    e1.grid(row=2, column=2)

    GetAnswers = Button(root, text="Perform Sentiment Analysis ", font="bold", fg="blue", command=lambda: sentiment(e1.get()))
    GetAnswers.grid(row=2, column=3)

    #main()

    root.mainloop()

