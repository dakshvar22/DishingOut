__author__ = 'daksh'

from dishingOut.SentimentAnalysis.antonymReplacer import AntonymReplacer
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import MaxentClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from sklearn import cross_validation
nltk.data.path.append("/home/daksh/Documents/Softwares/nltk_data")
import csv
import operator
import pickle

from nltk.classify import MaxentClassifier
from nltk.corpus import movie_reviews


def getBestWords(posWords,negWords):
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()

    for word in posWords:
        word_fd[word.lower()] += 1
        label_word_fd['pos'][word.lower()] += 1

    for word in negWords:
        word_fd[word.lower()] += 1
        label_word_fd['neg'][word.lower()] += 1

    pos_word_count = label_word_fd['pos'].N()
    neg_word_count = label_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}

    for word, freq in word_fd.items():
        pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
                                               (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
                                               (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score

    # best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:10000]
    sorted_x = sorted(word_scores.items(), key=operator.itemgetter(1),reverse=True)
    bestwords = set([w for w,s in sorted_x])

    return bestwords

def best_word_feats(words,bestwords):
    return dict([(word, True) for word in words if word in bestwords])

def word_feats(words):
    return dict([(word, True) for word in words])

def best_bigram_word_feats(words,posWords,negWords, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    bestwords = getBestWords(posWords,negWords)
    d.update(best_word_feats(words,bestwords))
    return d


posWords = list()
negWords = list()
with open('../data/finalPosWords.csv','r') as csvfile:
    spamreader = csv.reader(csvfile)
    posWords = list(spamreader)

with open('../data/finalNegWords.csv','r') as csvfile:
    spamreader = csv.reader(csvfile)
    negWords = list(spamreader)

posWords = [word[0] for word in posWords]
negWords = [word[0] for word in negWords]

bestwords = getBestWords(posWords,negWords)

# posfeats = [(best_word_feats(posWords,bestwords),'pos')]
# negfeats = [(best_word_feats(negWords,bestwords),'neg')]
posfeats = [(best_bigram_word_feats(posWords,posWords,negWords),'pos')]
negfeats = [(best_bigram_word_feats(negWords,posWords,negWords),'neg')]

trainfeats = negfeats + posfeats


algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
# classifier = nltk.MaxentClassifier.train(trainfeats, algorithm = 'gis',max_iter=3)
classifier = nltk.NaiveBayesClassifier.train(trainfeats)
# classifier.show_most_informative_features(10)
f = open('nb_classifier.pickle', 'wb')
# f = open('maxEnt_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()


sentence = "The chicken items were decent but the prawn was atrocious"
# replacer = AntonymReplacer()
#
l = sentence.split(' ')
# l = replacer.replace_negations(l)
# print(l)
# # l = ['We','had','good']
print(word_feats(l))
print(classifier.prob_classify(word_feats(l)).prob('pos'))
print(classifier.prob_classify(word_feats(l)).prob('neg'))