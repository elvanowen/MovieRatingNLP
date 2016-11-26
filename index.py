from TwitterSearch import *
import preprocessor as p
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk import pos_tag
import string
import re
from optparse import OptionParser
import sys

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def tokenize(tweet):
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(tweet.lower())
    print(tokens)

    no_punc_tokens = []
    for token in tokens:
        stripped = re.sub(r'\B[:,.!]\B', '', token)
        if stripped != '': no_punc_tokens.append(stripped)

    tokens_pos = pos_tag(no_punc_tokens)
    print(tokens_pos)
    for (word, tags) in tokens_pos:
        yield (word, tags)

def lemmatization(word, tags):
    lmt = WordNetLemmatizer()
    tag = get_wordnet_pos(tags)
    if tag != '': word = lmt.lemmatize(word, pos=tag)
    else: word = lmt.lemmatize(word)

    return word

def preprocess(tweet):
    preprocessed = ''

    # Since training data does not contain any hashtags or emojis or smilies
    # it is useless to have them, then just remove all of them
    # p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.NUMBER, p.OPT.RESERVED)
    tweet = p.clean(tweet)

    for (token, tags) in tokenize(tweet):
        word = lemmatization(token, tags)
        preprocessed += word + ' '

    return re.sub("\s\s+", ' ', preprocessed).strip()

parser = OptionParser()
parser.add_option("-m", "--movie", dest="movie", help="get tweets of movie title")

(options, args) = parser.parse_args()
movie = options.movie

if movie == '' or movie == None:
    print('Error. Usage: python index.py --movie "<movie>"')
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
        print()
        print("---------")
        print(tweet['text'])
        print(preprocessed)
        print("---------")

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)