#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
from bottle import get, post, request, run  # or route
import csv
from Classifier import NaiveBayes, Maxent, LogisticRegression, LinearSVC
from Sentiment import sentiment, cleanLine, deepClean

# Dictionary that used for testing purposes,
# if the classifier wasn't correct it holds the correct answer.
# Also all incorrect answers are saved into the file.
white_list = {}

# Form for the main page
@get('/')
@post('/')
def tweet():
    return '''
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>BIA660 Example</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
        <style type="text/css">
            .bs-example{
                margin: 20px;
            }
        </style>
        </head>
        <body>
        <br><br><br><br><br><br><br><br><br><br><br><br>
        <form action="/sentiment" method="post">

        <div align="middle" style="width: 40%; margin: 0px auto;">
        <img src="https://g.twimg.com/Twitter_logo_blue.png" height="100" width="110">
        <h1>TwitterLytics</h1>
        <h3>by Alek, Dmitry & Julian <br><br>
        <h2>Tweet: <input name="tweet" type="text" />
        <button type="submit" class="btn btn-primary">Get Sentiment</button></h2>
        </div>

        </form>
        </body>
        </html>
    '''


# Form for the page that analyze tweets
@post('/sentiment')
def do_tweet():
    tweet = request.forms.get('tweet')

    # clean tweet using predefined rules that are described in the Sentiment class
    clean_tweet = deepClean(cleanLine(tweet))

    # Check if tweet is in white list
    if clean_tweet in white_list:
        answer = white_list[clean_tweet]
    else:
        # Get an answer using the predefined classifier
        mySentiment = sentiment(classifier, clean_tweet)
        answer = {'pos': 'Positive', 'neg': 'Negative'}[mySentiment]
    return '''
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Output</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
        </head>
        <body>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br>

        <div align="middle" style="width: 40%; margin: 0px auto;">
        <h3>Tweet: {tweet} <br> <br>
        <code>{answer}</code> </h3> <br>


        <form action="/thanks" method="post">
            <button name="bla" type="submit" class="btn btn-primary">Correct</button>
            <button name="incorrect" type="submit" class="btn btn-primary">Incorrect</button>

            <input name="answer" value="{answer}" type="hidden" />
            <input name="tweet" value="{tweet}" type = "hidden" />
            <input name="clean_tweet" value="{clean_tweet}" type = "hidden" />
        </form>

        </div>
        </body>
        </html>


        '''.format(tweet=tweet, answer=answer, clean_tweet=clean_tweet)


# Form that is requesting verification of classification
@post('/classify')
def classify():
    return '''
    <p>What is the true sentiment?</p>
    <form action="/thanks" method="post">
            <input name="tweet" value="{tweet}" type = "hidden" />
            <input name="answer" value="Positive" type="submit" />
            <input name="answer" value="Negative" type="submit" />
    </form>
    '''.format(tweet=request.forms.get('tweet'))


# Thank you form, that display gratitude for verification
@post('/thanks')
def say_thanks():
    tweet = request.forms.get('tweet')
    answer = request.forms.get('answer')
    clean_tweet = request.forms.get('clean_tweet')

    # Write all checked tweets into the file
    if answer == 'Correct':
        data = [str(4), tweet]
    elif answer == 'Positive':
        data = [str(4), tweet]
        white_list[clean_tweet] = 'Negative'
    elif answer == 'Negative':
        data = [str(4), tweet]
        white_list[clean_tweet] = 'Positive'
    with open('results.csv', 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(data)

    # Go to initial page.
    post()
    return '''
    <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Example of Bootstrap 3 Vertical Form Layout</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
        <style type="text/css">
            .bs-example{
                margin: 20px;
            }
        </style>
        </head>
        <body>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        <form action="/" method="post">

        <div align="middle" style="width: 40%; margin: 0px auto;">

        <h2>Thanks for your feedback! <br> <br> <br>
        <button type="submit" class="btn btn-primary">Start Over</button></h2>
        </div>

        </form>
        </body>
        </html>
    '''


if len(sys.argv) == 2:
    choice = 'maxent'
else:
    choice = sys.argv[2].lower()

classifier_folder = sys.argv[1]


try:
    if choice == 'maxent':
        classifier = Maxent(classifier_folder)
    elif choice == 'logisticregression' or choice == 'logreg':
        classifier = LogisticRegression(classifier_folder)
    elif choice == 'linearsvc' or choice == 'svc':
        classifier = LinearSVC(classifier_folder)
    elif choice == 'naivebayes' or choice == 'nv':
        classifier = NaiveBayes(classifier_folder)
    else:
        raise
except:
    print "Classifier wasn't recognized"
    quit()

run(host='localhost', port=8080, debug=True)
