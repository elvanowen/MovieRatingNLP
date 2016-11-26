import nltk
import sys
import os
import time
import string
import re
import preprocessor as p

from nltk.corpus import wordnet
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk import pos_tag


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

def tokenize(text):
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(text.lower())
    # print(tokens)

    no_punc_tokens = []
    for token in tokens:
        stripped = re.sub(r'\B[:,.!]\B', '', token)
        if stripped != '': no_punc_tokens.append(stripped)

    tokens_pos = pos_tag(no_punc_tokens)
    # print(tokens_pos)
    for (word, tags) in tokens_pos:
        yield (word, tags)

def lemmatization(word, tags):
    lmt = WordNetLemmatizer()
    tag = get_wordnet_pos(tags)
    if tag != '': word = lmt.lemmatize(word, pos=tag)
    else: word = lmt.lemmatize(word)

    return word

def preprocess(text):
    preprocessed_word = [];

    for (token, tags) in tokenize(text):
        preprocessed_word.append(lemmatization(token, tags))

    return preprocessed_word

def usage():
    print("Usage:")
    print("python %s <data_dir>" % sys.argv[0])
   
data_dir = "aclImdb/test/"
classes = ['pos', 'neg']

# Read the data
train_data = []
train_labels = []
test_data = []
test_labels = []
# for curr_class in classes:
#     dirname = os.path.join(data_dir, curr_class)
#     for fname in os.listdir(dirname):
#         with open(os.path.join(dirname, fname), 'r') as f:
#             content = f.read()
#             if fname.startswith('cv9'):
#                 test_data.append(content)
#                 test_labels.append(curr_class)
#             else:
#                 train_data.append(content)
#                 train_labels.append(curr_class)

for curr_class in classes:
    dirname = os.path.join(data_dir, curr_class)
    fnamelist = os.listdir(dirname)
    # for fname in fnamelist[:11251]:
    for fname in fnamelist[0:100]:
        with open(os.path.join(dirname, fname), 'r', encoding="utf8") as f:
            content = f.read()
            lowers = content.lower()
            translator = str.maketrans({key: None for key in string.punctuation})
            no_punctuation = lowers.translate(translator)
            train_data.append(content)
            train_labels.append(curr_class)                
    # for fname in fnamelist[11251:]:
    for fname in fnamelist[100:110]:
        with open(os.path.join(dirname, fname), 'r', encoding="utf8") as f:
            content = f.read()
            lowers = content.lower()
            translator = str.maketrans({key: None for key in string.punctuation})
            no_punctuation = lowers.translate(translator)
            test_data.append(content)
            test_labels.append(curr_class) 

# Create feature vectors
vectorizer = TfidfVectorizer(tokenizer=preprocess, sublinear_tf=True)
train_vectors = vectorizer.fit_transform(train_data)
test_vectors = vectorizer.transform(test_data)

# Perform classification with SVM, kernel=rbf
classifier_rbf = svm.SVC()
t0 = time.time()
classifier_rbf.fit(train_vectors, train_labels)
t1 = time.time()
prediction_rbf = classifier_rbf.predict(test_vectors)
t2 = time.time()
time_rbf_train = t1-t0
time_rbf_predict = t2-t1

# # Perform classification with SVM, kernel=linear
# classifier_linear = svm.SVC(kernel='linear')
# t0 = time.time()
# classifier_linear.fit(train_vectors, train_labels)
# t1 = time.time()
# prediction_linear = classifier_linear.predict(test_vectors)
# t2 = time.time()
# time_linear_train = t1-t0
# time_linear_predict = t2-t1

# # Perform classification with SVM, kernel=linear
# classifier_liblinear = svm.LinearSVC()
# t0 = time.time()
# classifier_liblinear.fit(train_vectors, train_labels)
# t1 = time.time()
# prediction_liblinear = classifier_liblinear.predict(test_vectors)
# t2 = time.time()
# time_liblinear_train = t1-t0
# time_liblinear_predict = t2-t1

# Print results in a nice table
print("Results for SVC(kernel=rbf)")
print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
print(classification_report(test_labels, prediction_rbf))
# print("Results for SVC(kernel=linear)")
# print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
# print(classification_report(test_labels, prediction_linear))
# print("Results for LinearSVC()")
# print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
# print(classification_report(test_labels, prediction_liblinear))