#!/usr/bin/env python
import sys
import tweepy
import bitly_api
import time
import ConfigParser

# GPSbot by Felix Sargent (felix.sargent@gmail.com)
#
# GPSBot is designed to be used with twitter
# when you want to let someone know where you are
# just "@gpsbot @(friend) I'm here!"
# and gpsbot will send them a google maps link to your location

class Gpsbot(object):
  
  def __init__(self):
    config = ConfigParser.ConfigParser()
    config.read('gpsbot.cfg')
    CONSUMER_KEY = config.get('twitterapi','consumer_key')
    CONSUMER_SECRET= config.get('twitterapi','consumer_secret')
    ACCESS_KEY = config.get('twitterapi','access_key')
    ACCESS_SECRET = config.get('twitterapi','access_secret')
    BITLY_USERNAME = config.get('bitlyapi','bitly_username')
    BITLY_KEY = config.get('bitlyapi','bitly_key')
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    self.api = tweepy.API(auth)
    self.bitly = bitly_api.Connection(BITLY_USERNAME,BITLY_KEY)
    self.oldmentions = None
  
  
  def getUpdate(self):
    """Get gpsbot status"""
    try:
      self.mentions =  self.api.mentions()
    except:
      print "Could not retrieve mentions. Check the gpsbot.cfg for the right API keys."

  def is_valid(self):
     mention = self.mentions[0]
     if self.mentions[0].geo != None:
        return 1

  def print_latest_tweet(self):
    self.getUpdate()
    return self.mentions[0].user.screen_name + ": " + self.mentions[0].text

  def is_new(self):
    if self.oldmentions[0].id_str != self.mentions[0].id_str:
      return 1
    else: return 0


  def makeMessage(self):
    """Take the latest update and turn it into a response string"""
    try:
      mention = self.mentions[0]
    except AttributeError:
      getUpdate()
    #grab the coordinates
    lat =  mention.geo['coordinates'][0]
    lng =  mention.geo['coordinates'][1]
    #grab the sender and the text, remove "@gpsbot"
    sender = mention.user.screen_name
    rawtext = mention.text
    text_list = rawtext.split()
    for w in text_list:
      if w.lower() == "@gpsbot":
        text_list.remove(w)
    text = " ".join(text_list)
    #create the URL and shorten it
    url = 'http://maps.google.com/maps?q=%s+%s' % (lat,lng)
    shortUrl = self.bitly.shorten(url)
    self.response = "@"+ sender + " is here: " + shortUrl['url'] + " and says \"" + text + "\""
    print self.response
    return self.response

  def postResponse(self):
    self.api.update_status(self.response)

  def daemonize(self):
    while True:
      print "Polling!"
      self.poll()
      self.oldmentions = self.mentions
      time.sleep(60)
      self.getUpdate()

  def poll(self):
    if self.is_valid() and self.is_new() == 1:
      self.makeMessage()
      print "Valid tweet, replying with:", self.response
      self.postResponse()


  def main(self):
    choice = None
    while choice != "0":
        print \
        """GPSBOT - A Twitter Message Sender

        0 - Quit
        1 - Grab Updates
        2 - Make Message
        3 - Post Response
        4 - Daemonize
        """

        choice = raw_input("Choice: ")
        print

        if choice == "0":
          print ""

        elif choice == "1":
          self.getUpdate()

        elif choice == "2":
          if self.is_valid == 1:
            self.makeMessage()
          elif self.is_valid == 2: print "No Geo Coordinates:\n\t", self.print_latest_tweet()
          else: print "Could not grab tweets. Check the API keys in the gpsbot.cfg"

        elif choice == "3":
          try:
            self.postReponse()
            print "Responding with", self.response
          except:
            print "No response yet!"

        elif choice == "4":   # Daemonize
          self.getUpdate()
          self.oldmentions = self.mentions
          self.daemonize()

        #Unknown
        else:
          print "\nSorry, but", choice,"is not a valid choice."


if __name__ == "__main__":
  gpsbot = Gpsbot()
  gpsbot.main()
