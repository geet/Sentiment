import tweepy

CONSUMER_KEY = 'Wb4W1n264iHhcrqcXt54bA'
CONSUMER_SECRET = '2NFs7pO610XKQUOs5hPAz8wCEO4uxmP3111HPhsmgc'

def get_api(request):
	# set up and return a twitter api object
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api
