from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import numpy as np
import pandas
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

messages=[line.rstrip() for line in open("smsspamcollection/SMSSpamCollection")]
print len(messages)

messages=pandas.read_csv("smsspamcollection/SMSSpamCollection",sep="\t",quoting=csv.QUOTE_NONE, names=["label", "message"])


stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 


lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in messages.message] 

#print [doc for doc in doc_clean]


# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = np.asarray([dictionary.doc2bow(doc) for doc in doc_clean])
print doc_term_matrix

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamulticore.LdaMulticore

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=4 ,id2word = dictionary, chunksize=2000, passes=30)
print(ldamodel.print_topics(num_topics=4, num_words=25))

sample = dictionary.doc2bow(['great', 'news', 'call', 'freefone', '08006344447', 'claim', 'guaranteed', '\xc2\xa31000', 'cash', '\xc2\xa32000', 'gift', 'speak', 'live', 'operator', 'now'])
print ldamodel[sample]


#def identitfy_topic(input_message):

