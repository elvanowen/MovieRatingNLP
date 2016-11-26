import nltk
import os
import os.path
import time

from preprocess import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

def buildModel():
    traindata_dir = "aclImdb/train/"
    testdata_dir = "aclImdb/test/"
    classes = ['pos', 'neg']

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []

    for curr_class in classes:
        dirname = os.path.join(traindata_dir, curr_class)
        fnamelist = os.listdir(dirname)
        for fname in fnamelist:
            with open(os.path.join(dirname, fname), 'r', encoding="utf8") as f:
                content = f.read()
                train_data.append(content)
                train_labels.append(curr_class)
    for curr_class in classes:
        dirname = os.path.join(testdata_dir, curr_class)
        fnamelist = os.listdir(dirname)
        for fname in fnamelist:
            with open(os.path.join(dirname, fname), 'r', encoding="utf8") as f:
                content = f.read()
                test_data.append(content)
                test_labels.append(curr_class)

    # Create feature vectors
    vectorizer = TfidfVectorizer(tokenizer=preprocess, sublinear_tf=True)
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)
    with open("vectorizer.pkl", 'wb') as vectorizerFile:
        joblib.dump(vectorizer, vectorizerFile)

    # Perform classification with SVM, kernel=linear
    classifier = svm.LinearSVC()
    t0 = time.time()
    classifier.fit(train_vectors, train_labels)
    t1 = time.time()
    joblib.dump(classifier, 'model.pkl')
    
    prediction = classifier.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1
    
    # Print results in a nice table
    print("Results for SVC(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print(classification_report(test_labels, prediction))
    print(accuracy_score(test_labels, prediction) * 100 + "%")

    return vectorizer, classifier

def loadModel():
    vectorizer = joblib.load(open("vectorizer.pkl", "rb"))
    model = joblib.load('model.pkl')
    return vectorizer, model

def isModelExists():
    return os.path.isfile('model.pkl') and os.path.isfile('vectorizer.pkl')   