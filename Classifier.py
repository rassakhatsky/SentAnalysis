#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This class is used for uploading predefined classifier.
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pickle

# Function that upload a classifier by path
def getClassifier(filename):
    classifier = pickle.load(open(filename))
    return classifier


# Function for uploading the NaiveBayes classifier
def NaiveBayes(classifier_folder):
    return getClassifier(classifier_folder + 'tweets_NaiveBayes_03.pickle')


# Function for uploading the Maxent classifier
def Maxent(classifier_folder):
    return getClassifier(classifier_folder + 'tweets_Maxent.pickle')


# Function for uploading the Logistic Regression classifier
def LogisticRegression(classifier_folder):
    return getClassifier(classifier_folder + 'tweets_sklearn.LogisticRegression.pickle')


# Function for uploading the Linear SVC classifier
def LinearSVC(classifier_folder):
    return getClassifier(classifier_folder + 'tweets_sklearn.LinearSVC_01.pickle')
