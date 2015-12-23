import json
import csv
from pprint import pprint
import nltk
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
import nltk.tokenize.punkt
import re
import time

dishes = []
with open('dishes.csv') as f:
	data = csv.reader(f)
	for row in data:
		try:
			dishes.append(row[0].lower())
		except:
			pass
dishes = filter(lambda x: len(x)>2, list(set(dishes)))

total = 0
count=0
def filterReview(review):
	
	sentences = nltk.sent_tokenize(review)
	tokenizer = RegexpTokenizer(r'\w+')
	full=[]
	global total
	total += len(sentences)
	global count
	for sentence in sentences:
		for dish in dishes:
			if(dish in tokenizer.tokenize(sentence.lower())):
				full.append(sentence)
				count+=1
				break
	modifiedReview = ' '.join(full)
	return modifiedReview

def addDishes(review):
	print type(review)
	review = review.replace('\n','. ')
	review = re.sub(r'\.+', ". ", review)
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(review)
	tokenizer = RegexpTokenizer(r'\w+')
	full=defaultdict(list)
	global total
	total += len(sentences)
	global count
	for sentence in sentences:
		for dish in dishes:
			#~ if(re.search(r"\b"+dish+r"\b", sentence.lower())!=None):
			if(dish in sentence.lower()):
				full[dish].append(sentence)
				count+=1
	
	return dict(full)

with open('reviews.json') as data_file:
	data = json.load(data_file)
resCount=0
reviewCount=0
start = time.time()
for restaurant in data:
	try:
		resCount+=1
		reviews = restaurant['userReviews']
		rest_rev = []
		d = defaultdict(list)
		for review in reviews:
			reviewCount+=1
			dish_reviews = addDishes(review['reviewText'])
			for dish in dish_reviews.keys():
				d[dish].extend(dish_reviews[dish])
			rest_rev.append(dish_reviews)
			#~ modifiedReview = filterReview(review['reviewText'])
			#~ review['reviewText']=modifiedReview
			print reviewCount, resCount
		restaurant['dishes']=d
	except:
		pass
print total, count
print time.time()-start
with open('result.json','w') as fp:
	json.dump(data, fp, indent=2)


