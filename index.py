from TwitterSearch import *
import preprocessor as p
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import string
import nltk
import re
from optparse import OptionParser
import sys

def tokenize(sentences):
    '''Split sentences into constituent words'''
    for sent in nltk.sent_tokenize(sentences.lower()):
        for word in nltk.word_tokenize(sent):
            yield word

def lemmatization(word):
    '''Word stemmer; find the root of the word. E.g. 'dogs' becomes 'dog'''
    lmt = WordNetLemmatizer()
    word = word.lower()
    word = lmt.lemmatize(word)
    return word

def removePunctuation(s):
    '''Remove punctuation'''
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)

def preprocess(tweet):
    preprocessed = ''
    stemmer = LancasterStemmer()

    tweet = p.clean(tweet)

    for token in tokenize(tweet):
        word = lemmatization(removePunctuation(stemmer.stem(token)))
        preprocessed += word + ' '

    return re.sub("\s\s+", ' ', preprocessed).strip()

parser = OptionParser()
parser.add_option("-m", "--movie", dest="movie", help="get tweets of movie title")

(options, args) = parser.parse_args()
movie = options.movie

if movie == '':
    sys.exit()

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([movie]) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'kbibzVdoRoKOwd3dlxZCobum5',
        consumer_secret = 'qEz32mJANlQ5hbFGacxmMfO2Pmyexs3WgPFeGq4QzA88qAOKe8',
        access_token = '1348353366-ofrMAMNiFfz102VY9c3MXdTrsAD2c4Dq91QiWVD',
        access_token_secret = 'Io7orEnOvE2Rv2sdiASLRkLTVFA93DmSyF4r1i9CYQCXn'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        preprocessed = preprocess(tweet['text'])

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)