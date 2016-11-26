import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk import pos_tag
import preprocessor as p
import string
import re

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

    no_punc_tokens = []
    for token in tokens:
        stripped = re.sub(r'\B[:,.!]\B', '', token)
        if stripped != '': no_punc_tokens.append(stripped)

    tokens_pos = pos_tag(no_punc_tokens)
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