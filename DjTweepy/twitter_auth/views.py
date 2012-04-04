# Create your views here.
import tweepy
from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
import pickle,hashlib 
import data_preprocess
import pickle
from collections import defaultdict
from django.contrib.auth import authenticate, login
from twitter_auth.models import data_set,pos_tokens,neg_tokens,tweet_category_count,token_category_count
from utils import *
from naivebayesclassifier import NaiveBayesClassifier

def main(request):
        """
        main view of app, either login page or info page
        """
        # if we haven't authorised yet, direct to login page
        if check_key(request):
                return HttpResponseRedirect(reverse('info'))
        else:
                return render_to_response('twitter_auth/login.html')
 
def unauth(request):
        """
        logout and remove all session data
        """
        if check_key(request):
                api = get_api(request)
                request.session.clear()
                logout(request)
        return HttpResponseRedirect(reverse('main'))

def info(request):
        """
        display some user info to show we have authenticated successfully
        """
        if check_key(request):
                api = get_api(request)
                user = api.me()
                return render_to_response('twitter_auth/info.html', {'user' : user})
        else:
                return HttpResponseRedirect(reverse('main'))

def auth(request):
        # start the OAuth process, set up a handler with our details
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # direct the user to the authentication url
    auth_url = oauth.get_authorization_url()
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['unauthed_token_tw'] = (oauth.request_token.key, oauth.request_token.secret) 
    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    oauth.set_request_token(token[0], token[1])
    # get the access token and store
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error, failed to get access token'
    request.session['access_key_tw'] = oauth.access_token.key
    request.session['access_secret_tw'] = oauth.access_token.secret
    response = HttpResponseRedirect(reverse('info'))
    return response

def check_key(request):
        """
        Check to see if we already have an access_key stored, if we do then we have already gone through 
        OAuth. If not then we haven't and we probably need to.
        """
        try:
                access_key = request.session.get('access_key_tw', None)
                if not access_key:
                        return False
        except KeyError:
                return False
        return True









#Code to retrieve tweets
def getTweets(request):
            # == OAuth Authentication ==
            #
            # This mode of authentication is the new preferred way
            # of authenticating with Twitter.

            # The consumer keys can be found on your application's Details
            # page located at https://dev.twitter.com/apps (under "OAuth settings")
            consumer_key="Wb4W1n264iHhcrqcXt54bA"
            consumer_secret="2NFs7pO610XKQUOs5hPAz8wCEO4uxmP3111HPhsmgc"

            # The access tokens can be found on your applications's Details
            # page located at https://dev.twitter.com/apps (located 
            # under "Your access token")
            access_token="36641014-28RR3YAp6MxFxJ706gsp5a7bRy0sYDsjLCwixs2iM"
            access_token_secret="qOGQg84VvurJKX9qSF3Zgl973BxF6ryt7Yruoxtw"

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
                
            api = tweepy.API(auth)
            query = request.POST.get('query')	
            # If the authentication was successful, you should
            # see the name of the account print out
            result = api.search(query,rpp=500)
            #Convert each tweet in the result to string
            #and add it to a list
            tweets=[query]
           # tweets=[]
            for tweet in result:
                    try:
                            tweets.append(str(tweet.text))
                    except:
                            pass
            #pickle the list of tweets and save in file
            #for later use by function save_tweets
            current_tweets=open('current_tweets.txt','wb')
            pickle.dump(tweets,current_tweets)
            return render_to_response('twitter_auth/tweets.html',{'tweets':tweets})






def login_user(request):
    state = "Please login below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return render_to_response('base.html')
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
            
    return render_to_response('auth.html',{'state':state, 'username': username})




def save_tweets(request):
        #unpickle the list of recent tweets retrieved
        with open('current_tweets.txt','rb') as file_id:
                current_tweets=pickle.load(file_id)
        tokens=[]
        
        """Examine every Post variable one by one
        and write the positive and negative marked tweets
        into corresponding files after breaking the
        tweets into tokens"""
        m = hashlib.md5()
        for index in request.POST:
                (ind,a)=index.split(':')
                if request.POST.get(index,''):
                        if(request.POST[index]=='pos'):
                                out_file=open("positive.txt",'a')
                                m.update(current_tweets[int(a)-1])		
                                p=data_set(tweet=current_tweets[int(a)-1],tweet_hash=m.hexdigest(),pos_neg='pos',movie_name=current_tweets[0])
                                p.save()
                                #Update the number of positive tweets seen so far
                                try:
                                        p=tweet_category_count.objects.get(id=1)
                                        p.positive_count=p.positive_count+1
                                        p.save()
                                except:
                                         p=tweet_category_count(id=1,positive_count=1,negative_count=0)
                                         p.save()
                        else: 
				 
                                out_file=open("negative.txt",'a')
                                m.update(current_tweets[int(a)-1])
                                p=data_set(tweet=current_tweets[int(a)-1],tweet_hash=m.hexdigest(),pos_neg='neg',movie_name=current_tweets[0])
                                p.save()
                                #Update the number of negative tweets seen so far
                                try:
                                        p=tweet_category_count.objects.get(id=1)
                                        p.negative_count=p.negative_count+1
                                        p.save()
                                except:
                                        p=tweet_category_count(id=1,positive_count=0,negative_count=1)
                                        p.save()
                        tokens=current_tweets[int(a)-1].split()
                        #Removing noise words,names (@) and hyperlinks from the tweets
                        data_preprocess.remove_noise_words(tokens)
                        data_preprocess.remove_names(tokens)
                        data_preprocess.remove_links(tokens)
			#Removing the name of movie from the token list
                        movieName = current_tweets[0].split()
                        tokens = set(tokens)-set(movieName)
           
                        for token in tokens:
                                out_file.write(token+'\n')
                                if(request.POST[index]=='pos'):
                                        try:
                                                q=token_category_count.objects.get(id=1)
                                                q.positive_count=q.positive_count+1
                                                q.save()
                                        except:
                                                p=token_category_count(id=1,positive_count=1,negative_count=0)
                                                p.save()
                                        try:
                                                q=pos_tokens.objects.get(ptoken=token)
				#Adding 1 to the count of positive tokens
                                                q.pcount = q.pcount + 1
                                                q.save()
                                        except:
                                                r = pos_tokens(ptoken=token,pcount=1)
                                                r.save()
                                else:
                                        try:
                                                q=token_category_count.objects.get(id=1)
                                                q.negative_count=q.negative_count+1
                                                q.save()
                                        except:
                                                p=token_category_count(id=1,positive_count=0,negative_count=1)
                                                p.save()
                                        try:
                                                q=neg_tokens.objects.get(ntoken=token)
				#Adding 1 to the count of negative tokens
                                                q.ncount = q.ncount + 1
                                                q.save()
                                        except:
                                                r = neg_tokens(ntoken=token,ncount=1)
                                                r.save()	

        return render_to_response("tweetsSaved.html")
        
def user_movie_search(request):
        return render_to_response('user.html')

def classify_tweets(request):
        consumer_key="Wb4W1n264iHhcrqcXt54bA"
        consumer_secret="2NFs7pO610XKQUOs5hPAz8wCEO4uxmP3111HPhsmgc"
        access_token="36641014-28RR3YAp6MxFxJ706gsp5a7bRy0sYDsjLCwixs2iM"
        access_token_secret="qOGQg84VvurJKX9qSF3Zgl973BxF6ryt7Yruoxtw"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        query = request.POST.get('query')
        result=api.search(query)
        tweets=[]
        classification=[]
        for tweet in result:
                    try:
                            tweets.append(str(tweet.text))
                    except:
                            pass
        posScore=0
        negScore=0
        for tweet in tweets:
                tokens=tweet.split()
                data_preprocess.remove_noise_words(tokens)
                data_preprocess.remove_names(tokens)
                data_preprocess.remove_links(tokens)
                tweet_counts=[]
                token_counts=[]
                category_counts=defaultdict(lambda:defaultdict(int))
                p=tweet_category_count.objects.get(id=1)
                tweet_counts.append(p.positive_count)
                tweet_counts.append(p.negative_count)
                p=token_category_count.objects.get(id=1)
                token_counts.append(p.positive_count)
                token_counts.append(p.negative_count)
                for token in tokens:
                        try:
                                p=pos_tokens.objects.get(ptoken=token)
                                category_counts[token]['pos']=p.pcount
                        except:
                                category_counts[token]['pos']=0
                for token in tokens:
                        try:
                                p=neg_tokens.objects.get(ntoken=token)
                                category_counts[token]['neg']=p.ncount
                        except:
                                category_counts[token]['neg']=0
		
		
                classifier=NaiveBayesClassifier()
                result=classifier.classify(tokens,category_counts,tweet_counts,token_counts)
                if(result=='pos'):
                        posScore+=1
                else:
                        negScore+=1
                classification.append(result)
        return render_to_response("index.html",{'tweets':tweets,'pos_neg':classification,'posScore':posScore,'negScore':negScore})
