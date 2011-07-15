from twitter import *
import bitlyapi

"""
Twitter library by Mike Verdone from here: http://pypi.python.org/pypi/twitter
"""

class GPSbot(object):
   
    def __init__(self):
        self.twitter = Twitter("gpsbot", "0440offo")
        #geocoder = geocoders.Google("ABQIAAAAEcWGrCchXvTrYENi-q2auRQSuXh_XO-BzI6x1h_Y8jzQ5D583xQ79z24_sKzt5E3knCZgkWktfkzcQ")
        self.bitly = bitlyapi.BitLy("antagonist77", "R_d919ec73564a5b6f513c4f2d9fec0175")
        print "Twitter GPSBot Started!\n\n"
    

    def getUpdate(self):
        """Get Latest Update"""
        self.mentions = self.twitter.statuses.mentions()
        return self.mentions
    
    def makeMessage(self):
        """Take the latest update and turn it into a response string"""
        try:
            #grab the coordinates
            mention =  self.mentions[0]
            lat =  mention["coordinates"]["coordinates"][1]
            lng =  mention["coordinates"]["coordinates"][0]
            #grab the sender and the text, remove "@gpsbot"
            sender = mention["user"]["screen_name"]
            rawtext = mention["text"]
            text = rawtext.replace("@gpsbot ","")            
            #create the URL and shorten it
            url = 'http://maps.google.com/maps?q=%s+%s' % (lat,lng)
            shortUrl = self.bitly.shorten(longUrl=url)
            self.response = "@"+ sender + " is here: " + shortUrl['url'] + " and says \"" + text + "\""
            return self.response
            
        except TypeError:
            print "No GPS coordinates found."     

    def postResponse(self):
        print "Sending: " + self.response
        self.twitter.statuses.update(status = self.response)
        
    def main(self):
        choice = None
        self.getUpdate()
        self.makeMessage()
        print "Created: " + self.response
        while choice != "0":
            print \
            """Twitter Message Sender
            
            0 - Quit
            1 - Grab Updates
            2 - Post Response
            """

            choice = raw_input("Choice:")
            print
            
            #exit
            if choice == "0":
                print "Good-Bye."
            
            #Listen
            elif choice == "1":
                self.getUpdate()
                self.makeMessage()
                
            elif choice == "2":
                self.postResponse()
                
            #Unknown
            else:
                print "\nSorry, but", choice,"is not a valid choice."
        
        
            
gpsbot = GPSbot()
gpsbot.main()
raw_input("\n\nPress the enter key to exit.")        
