from TwitterSearch import *
from optparse import OptionParser
import sys
import preprocess
import model

parser = OptionParser()
parser.add_option("-m", "--movie", dest="movie", help="get tweets of movie title")

(options, args) = parser.parse_args()
movie = options.movie

if movie == '' or movie == None:
    print('Error. Usage: python index.py --movie "<movie>"')
    sys.exit()

try:
    tso = TwitterSearchOrder()
    tso.set_keywords([movie])
    tso.set_language('en')
    tso.set_include_entities(False)

    ts = TwitterSearch(
        consumer_key = 'kbibzVdoRoKOwd3dlxZCobum5',
        consumer_secret = 'qEz32mJANlQ5hbFGacxmMfO2Pmyexs3WgPFeGq4QzA88qAOKe8',
        access_token = '1348353366-ofrMAMNiFfz102VY9c3MXdTrsAD2c4Dq91QiWVD',
        access_token_secret = 'Io7orEnOvE2Rv2sdiASLRkLTVFA93DmSyF4r1i9CYQCXn'
    )

    numberOfTweets = 1
    tweets = []

    # Start building models
    classifier = model.buildModel()

    for tweet in ts.search_tweets_iterable(tso):
        preprocessed = preprocess.preprocess(tweet['text'])
        tweets.append(preprocessed)
        # print("---------")
        # print(tweet['text'])
        # print(preprocessed)
        # print("---------")
        if numberOfTweets == 100: break
        else: numberOfTweets = numberOfTweets + 1

        # Calculate Ratings based on already obtained tweets
        # Calculation is done real time, based on the number of tweets fetched
        if numberOfTweets % 100 == 0:
            # Code
            # Code
            # Code

            # Print Movie ratings
            # print(movie.title() + " Rating : " + rating, end='\r')

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)