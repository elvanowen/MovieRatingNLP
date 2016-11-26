from math import sqrt
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess import preprocess

def confidence(ups, downs):
	#code from http://stackoverflow.com/questions/10029588/python-implementation-of-the-wilson-score-interval
    n = ups + downs

    if n == 0:
        return 0

    z = 1.0 #1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return ((phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))

def countRating(vectorizer, classifier, tweets):
	test_vectors = vectorizer.transform(tweets)
	prediction_rbf = classifier.predict(test_vectors)
	pos = prediction_rbf.count('pos')
	neg = prediction_rbf.count('neg')
	print (confidence(pos,neg))
	return confidence(pos,neg)