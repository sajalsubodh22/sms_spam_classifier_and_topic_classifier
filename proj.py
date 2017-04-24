import matplotlib.pyplot as plt
import csv
###from textblob import TextBlob
import pandas
import sklearn
import numpy as np
from time import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB , GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.decomposition import NMF, LatentDirichletAllocation
##from sklearn.grid_search import GridSearchCV
##from sklearn.cross_validation import StratifiedKFold, cross_val_score, train_test_split 
from sklearn.tree import DecisionTreeClassifier 


messages=[line.rstrip() for line in open("smsspamcollection/SMSSpamCollection")]
print len(messages)

messages=pandas.read_csv("smsspamcollection/SMSSpamCollection",sep="\t",quoting=csv.QUOTE_NONE, names=["label", "message"])
 ###messages.groupby('label').describe()

SPLIT_PERC = 0.75
split_size = int(len(messages)*SPLIT_PERC)
x_train = messages.message[:split_size]
x_test = messages.message[split_size:]
y_train = messages.label[:split_size]
y_test = messages.label[split_size:]

"stop words"
english = ["a", "about", "above", "across", "after", "afterwards", 
			"again", "against", "all", "almost", "alone", "along", 
			"already", "also","although","always","am","among", "amongst", 
			"amoungst", "amount",  "an", "and", "another", "any","anyhow",
			"anyone","anything","anyway", "anywhere", "are", "around", "as",  
			"at", "back","be","became", "because","become","becomes", "becoming", 
			"been", "before", "beforehand", "behind", "being", "below", "beside", 
			"besides", "between", "beyond", "bill", "both", "bottom","but", "by", 
			"call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", 
			"de", "describe", "detail", "do", "done", "down", "due", "during", "each", 
			"eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", 
			"etc", "even", "ever", "every", "everyone", "everything", "everywhere", 
			"except", "few", "fifteen", "fify", "fill", "find", "fire", "first", 
			"five", "for", "former", "formerly", "forty", "found", "four", "from", 
			"front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", 
			"he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", 
			"hers", "herself", "him", "himself", "his", "how", "however", "hundred", 
			"ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", 
			"keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", 
			"me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", 
			"much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", 
			"nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", 
			"often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", 
			"ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", 
			"see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", 
			"since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", 
			"sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", 
			"them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", 
			"thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", 
			"throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", 
			"two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", 
			"whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", 
			"wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", 
			"with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

print len(english)
"vectorizer"
vec=CountVectorizer(stop_words="english")
vec.fit(np.asarray(x_train))
###print vec.vocabulary_
counts = vec.transform(np.asarray(x_train)).todense()

tfidf = TfidfTransformer(norm='l2')
tfidf.fit(counts)
###print tfidf.idf_
features_train = tfidf.transform(counts).todense()



"""Classification using different models"""
labels_train=np.asarray(y_train)
clf = MultinomialNB()
#clf = GaussianNB()
#clf = SVC(kernel="rbf")
#clf =DecisionTreeClassifier()
t0=time()
clf.fit(features_train,labels_train)
print "time for multinomial NB: ",round(time()-t0,3), "seconds"

counts2=vec.transform(x_test).todense()
features_test=tfidf.fit_transform(counts2).todense()
pred=clf.predict(features_test)
labels_test=np.asarray(y_test)
print accuracy_score(labels_test,pred)

"""confusion matrics"""
print confusion_matrix(labels_test,pred)



def inpt(input_message):
	input_mess=pandas.Series(input_message)
	print input_mess
	input1=vec.transform(np.asarray(input_mess)).todense()
	feature_input=tfidf.fit_transform(input1).todense()
	pred=clf.predict(feature_input)
	if np.array_equal(pred,['spam']):
		result ="spam"
	else : 
		result="ham"
	return result