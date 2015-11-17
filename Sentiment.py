#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import nltk
from nltk.util import ngrams
from nltk.corpus import wordnet as wn
import re
from nltk.stem.wordnet import WordNetLemmatizer

URL = 'URL'
USERNAME = 'USERNAME'

# Make a feature vector
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


# Function returns part of speech only for Nouns, Verbs, Adverbs and Adjectives
def get_speechpart4lemm(part_of_speech):
    if part_of_speech in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif part_of_speech in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    elif part_of_speech in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif part_of_speech in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    else:
        return None


# Use lemmatizer to achive the base form of words
def clean_word(term):
    lemmatizer = WordNetLemmatizer()
    type = get_speechpart4lemm(term[1])
    word = None
    if type != None:
        word = lemmatizer.lemmatize(term[0], type)
    return word


# Additional cleaning
def deepClean(sentence):
    sentence = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(sentence)
    result = []
    for tag in tags:
        tmp = clean_word(tag)
        if tmp != None:
            result.append(clean_word(tag))
    result.append('.')
    result = ' '.join(result)
    return result


# Clean line of text
def cleanLine(self):
    self = self.lower()
    # Convert any links (www.* | https?://*) to URL
    self = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', URL, self)
    # Convert @username to USERNAME
    self = re.sub('@[^\s]+', USERNAME, self)
    # Remove additional white spaces
    self = re.sub('[\s]+', ' ', self)
    # Replace hashtag to normal word (#tag > tag)
    self = re.sub(r'#([^\s]+)', r'\1', self)
    self = self.strip('\'"')
    return self


# Function that used for sentiment analysis of tweets
def sentiment(classifier, text):
    tweet = text.split(' ')
    set = dict([(word, True) for word in tweet])

    #
    myNGRAM = ngrams(tweet, 2)
    for n in myNGRAM:
        set[n] = True
    result = classifier.classify(set)

    # in training data negative and positive tweets were classified in the opposite categories, so the result has to be swapped again
    result = {'neg': 'pos', 'pos': 'neg'}[result]
    return result
