from math import sqrt
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess import preprocess

def countRating(pos, neg):
    n = pos + neg

    if n == 0:
        return 0

    z = 1.0 #1.44 = 85%, 1.96 = 95%
    phat = float(pos) / n
    return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))

def getRating(vectorizer, classifier, tweets):
	test_vectors = vectorizer.transform(tweets)
	prediction_rbf = classifier.predict(test_vectors)
	pos = (prediction_rbf=='pos').sum()
	neg = (prediction_rbf=='neg').sum()
	return countRating(pos,neg)