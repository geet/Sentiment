from django.conf.urls.defaults import *
from twitter_auth.views import *

urlpatterns = patterns('twitter_auth.views',
    url(r'^$', view=main, name='main'),
    url(r'^callback/$', view=callback, name='auth_return'),
    url(r'^logout/$', view=unauth, name='oauth_unauth'),
    url(r'^auth/$', view=auth, name='oauth_auth'),
    url(r'^info/$', view=info, name='info'),
    url(r'^savetweets',view=save_tweets,name='save_tweets'),
    url(r'^user',view=user_movie_search,name='user_movie_search'),
    url(r'^classifiedtweets',view=classify_tweets,name='classify_tweets'),
)
