import pandas as pd
import nltk
# nltk.download()  - enélkül nem mukodott a stopwords list amig felnem raktam minden komponenst
# nltk.download()
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.collocations import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import ngrams
from collections import Counter

lem = WordNetLemmatizer()

# ps = PorterStemmer()

df=pd.read_excel('orban-thisyear-translated.xlsx')


tokenizedword = []
tokentext = []

for i in df.Text:
    tokenizedword.append(word_tokenize(str(i)))

for i in df.Text:
    tokentext.append(sent_tokenize(str(i)))

allSentences = ''
for wordList in tokentext:
    allSentences += str(wordList)

allWords = []
for wordList in tokenizedword:
    allWords += wordList

for i in range(len(allWords)):
    allWords[i] = allWords[i].lower()

# stop_words=set(stopwords.words("hungarian"))
stop_words = nltk.corpus.stopwords.words('english')

custom_stopWorlds = [",",":","-","!",'\"',".","(",")","also", "photo", "\"", "would","said", "?","viktor","one","according","even","\'s","percent","since","n't","already","-"]
stop_words.extend(custom_stopWorlds)

filtered_list = []
for w in allWords:
    if w not in stop_words:
        filtered_list.append(w)

lemmatized_words = []
for w in filtered_list:
    lemmatized_words.append(lem.lemmatize(w))

fdist = FreqDist(lemmatized_words)
print(fdist)
print(fdist.most_common(50))

fdist.plot(30,cumulative=False)
plt.show()

# COLLOCATIONS
# most common bigrams>
colText = nltk.Text(lemmatized_words)
colText.collocations(50)
# NGRAMS / 4words / first 5 result

# colngrams = list(nltk.ngrams(colText, 4)) 

# print(colngrams[:20])


# most common ngrams together
ngram1 = Counter(ngrams(allSentences.split(),7))
printngram1 = ngram1.most_common(20)
for i in printngram1:
    print(i)



# trigram_measures = nltk.collocations.TrigramAssocMeasures()
# orban_filter = lambda *w: 'Orbán' not in w

# finder = TrigramCollocationFinder.from_words(tokanized_text)
# finder.apply_freq_filter(2)
# finder.apply_ngram_filter(orban_filter)
# print (finder.nbest(trigram_measures.likelihood_ratio, 10))
