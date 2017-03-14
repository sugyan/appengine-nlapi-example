# -*- coding: utf-8 -*-
import os
import logging
import tweepy
import requests_toolbelt.adapters.appengine

from flask import Flask, render_template, request

requests_toolbelt.adapters.appengine.monkeypatch()
app = Flask(__name__)


def collect_tweets(target):
    auth = tweepy.AppAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    api = tweepy.API(auth)
    try:
        texts = []
        for status in api.user_timeline(target, include_rts=False, count=100, exclude_replies=True):
            texts.append(status.text)
        return '\n'.join(texts)
    except tweepy.error.TweepError:
        return ''


def analyze(target):
    text = collect_tweets(target)
    if text == '':
        return '取得できませんでした'
    return text


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
