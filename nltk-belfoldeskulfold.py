# TODO behuzni a kulfold es belfold cikkeket és ráereszteni egy most common ngramot

import pandas as pd
import nltk
from nltk import ngrams
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize


df=pd.read_excel('------.xlsx')

tokentext = []

for i in df.Text:
    tokentext.append(sent_tokenize(str(i)))


allSentences = ''
for wordList in tokentext:
    allSentences += str(wordList)

ngram = Counter(ngrams(allSentences.split(),10))
printngram = ngram.most_common(20)
for i in printngram:
    print(i)