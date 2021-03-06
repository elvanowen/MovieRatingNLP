from TwitterSearch import *
from optparse import OptionParser
import sys
import preprocess
import model
import rating
from log import log

parser = OptionParser()
parser.add_option("-m", "--movie", dest="movie", help="get tweets of movie title")

(options, args) = parser.parse_args()
movie = options.movie

if movie == '' or movie == None:
    print('Error. Usage: python index.py --movie "<movie>"')
    sys.exit()

try:
    numberOfTweets = 1
    tweets = []
    ratingValue = 0

    if model.isModelExists():
        print("Loading Classifier Model...")        
        vectorizer, classifier = model.loadModel()
    else:
        print("Building Classifier Model...")
        # Start building models
        vectorizer, classifier = model.buildModel()

    print("Retrieving Tweets...")
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
    for tweet in ts.search_tweets_iterable(tso):
        preprocessed = preprocess.preprocess(tweet['text'])
        tweets.append(preprocessed)

        log(tweet['text'] + '\nLABELS : ' + str(classifier.predict(vectorizer.transform([preprocessed]))[0]).upper())

        # print("---------")
        # print(tweet['text'])
        # print(preprocessed)
        # print("---------")
        if numberOfTweets == 1000: break
        else: numberOfTweets = numberOfTweets + 1

        # Calculate Ratings based on already obtained tweets
        # Calculation is done real time, based on the number of tweets fetched
        if (numberOfTweets % 10) == 0:
            ratingValue = rating.getRating(vectorizer, classifier, tweets)

            # Print Movie ratings
            print('{} Rating ({} tweets) : {} / 5.0'.format(movie.title(),  numberOfTweets, float("{0:.3f}".format(ratingValue * 5))), end='\r')

    # Print Movie ratings
    print(end='\r')
    print('{} Rating ({} tweets) : {} / 5.0'.format(movie.title(),  numberOfTweets, float("{0:.3f}".format(ratingValue * 5))))

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)