# -*- coding: utf-8 -*-
import os
import logging
import random
import tweepy
import requests_toolbelt.adapters.appengine

from flask import Flask, render_template, request
from google.cloud import language
from google.cloud.language.entity import EntityType

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


def process(text):
    language_client = language.Client()
    document = language_client.document_from_text(text)
    annotated = document.annotate_text(include_syntax=False)

    # calculate total score
    total_score = 0.0
    for sentence in annotated.sentences:
        total_score += sentence.sentiment.magnitude * sentence.sentiment.score
    # extract entities
    entities = set()
    for entity in annotated.entities:
        if entity.entity_type not in [EntityType.OTHER, EntityType.UNKNOWN]:
            entities.add(entity.name)

    return total_score, entities


@app.route('/analyze', methods=['POST'])
def analyze():
    screen_name = request.form['screen_name']
    text = collect_tweets(screen_name)
    if text == '':
        return render_template('error.html')

    total_score, entities = process(text)
    comment = 'ポジティブ！' if total_score > 0.0 else 'ネガティブ！'
    if abs(total_score) > 10.0:
        comment = 'とっても' + comment
    elif abs(total_score) > 5.0:
        comment = 'かなり' + comment
    else:
        comment = 'どちらかというと' + comment
    samples = random.sample(entities, min(7, len(entities)))
    return render_template('result.html',
                           screen_name=screen_name,
                           total_score=total_score,
                           comment=comment.decode('utf-8'),
                           samples=samples)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
