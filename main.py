# -*- coding: utf-8 -*-
import os
import logging
import random
import tweepy
import requests_toolbelt.adapters.appengine

from flask import Flask, render_template, request
from google.cloud import language

requests_toolbelt.adapters.appengine.monkeypatch()
app = Flask(__name__)


def collect_tweets(target):
    auth = tweepy.AppAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    api = tweepy.API(auth)
    try:
        tweets = []
        for status in api.user_timeline(target, include_rts=False, count=100, exclude_replies=True):
            tweets.append(status.text)
        return '\n'.join(tweets)
    except tweepy.error.TweepError:
        return ''


def analyze(target):
    text = collect_tweets(target)
    if text == '':
        return '取得できませんでした'

    language_client = language.Client()
    document = language_client.document_from_text(text)
    annotated = document.annotate_text(include_syntax=False)

    entity_names = set([entity.name.encode('utf-8') for entity in annotated.entities if entity.entity_type != 'OTHER'])
    total_score = sum([sentence.sentiment.magnitude * sentence.sentiment.score for sentence in annotated.sentences])
    return '@{} さんは {} などを呟いています。全体的なポジティブ度合いは… {}！'.format(
        target,
        ''.join(['「{}」'.format(x) for x in random.sample(entity_names, 7)]),
        total_score)


@app.route('/diagnose', methods=['POST'])
def diagnose():
    screen_name = request.form['screen_name']
    result = analyze(screen_name)
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
