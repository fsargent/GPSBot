import tweepy
token='b8tIIaVNf5uet7OFkqaf8w'
secret='2bAcRYLQWp00At3HA1Knzm2JS3IXTs2fonlImGr0X8'

auth = tweepy.OAuthHandler(token, secret)

try:
  redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
  print 'Error! Failed to get request token.'


print 'Please Authorize: ' + redirect_url
verifier = raw_input('Verifier: ').strip()

try:
  auth.get_access_token(verifier)
except tweepy.TweepError:
  print 'Error! Failed to get access token.'

api = tweepy.API(auth)
print "ACCESS_KEY = '%s'" % auth.access_token.key
print "ACCESS_SECRET = '%s'" % auth.access_token.secret
