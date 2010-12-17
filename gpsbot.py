#!/usr/bin/env python
import sys
import tweepy
import bitly_api


class Gpsbot(object):

  def __init__(self):
    CONSUMER_KEY = 'b8tIIaVNf5uet7OFkqaf8w'
    CONSUMER_SECRET = '2bAcRYLQWp00At3HA1Knzm2JS3IXTs2fonlImGr0X8'
    ACCESS_KEY = '151351658-Vs6EQ2mXF2X3xipBxMA9X8LFyKo1BMmwgKCy7Lc2'
    ACCESS_SECRET = 'OnmccOtTZin91wrRaJk3Oe75Sw8gm7FFSdte96l92s'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    self.api = tweepy.API(auth)
    self.bitly = bitly_api.Connection("antagonist77", "R_d919ec73564a5b6f513c4f2d9fec0175")

    
  def getUpdate(self):
    """Get gpsbot status"""
    self.mentions =  self.api.mentions()

  def makeMessage(self):
    """Take the latest update and turn it into a response string"""
    try:
      #grab the coordinates
      mention =  self.mentions[0]
      lat =  mention.place['bounding_box']['coordinates'][0][0][1]
      lng =  mention.place['bounding_box']['coordinates'][0][0][0]
      #grab the sender and the text, remove "@gpsbot"
      sender = mention.user.screen_name
      rawtext = mention.text
      text = rawtext.replace("@gpsbot ","")
      #create the URL and shorten it
      url = 'http://maps.google.com/maps?q=%s+%s' % (lat,lng)
      shortUrl = self.bitly.shorten(url)
      self.response = "@"+ sender + " is here: " + shortUrl['url'] + " and says \"" + text + "\""
      return self.response

    except TypeError:
      print "No GPS coordinates found."

  def postResponse(self):
    self.api.update_status(self.response)

  def main(self):
    choice = None
   # self.getUpdate()
   # self.makeMessage()
   # print "Created: " + self.response
    while choice != "0":
        print \
        """Twitter Message Sender

        0 - Quit
        1 - Grab Updates
        2 - Post Response
        """

        choice = raw_input("Choice:")
        print

        if choice == "0":
          print ""

        elif choice == "1":
          self.getUpdate()
          self.makeMessage()
          print self.response

        elif choice == "2":
          self.postResponse()

        #Unknown
        else:
          print "\nSorry, but", choice,"is not a valid choice."



gpsbot = Gpsbot()
gpsbot.main()
raw_input("\n\nPress enter key to exit.")

