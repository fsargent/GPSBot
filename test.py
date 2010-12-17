#!/usr/bin/env python
import sys
import tweepy



CONSUMER_KEY = 'b8tIIaVNf5uet7OFkqaf8w'
CONSUMER_SECRET = '2bAcRYLQWp00At3HA1Knzm2JS3IXTs2fonlImGr0X8'
ACCESS_KEY = '151351658-Vs6EQ2mXF2X3xipBxMA9X8LFyKo1BMmwgKCy7Lc2'
ACCESS_SECRET = 'OnmccOtTZin91wrRaJk3Oe75Sw8gm7FFSdte96l92s'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
