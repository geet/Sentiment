from django.conf.urls.defaults import *
from django.conf import settings
from twitter_auth import views
import settings	
urlpatterns = patterns('',
	# serve any media files (including css and javascript) while in development
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    # redirect all urls to the twitter_auth app
    (r'^', include('twitter_auth.urls')),
    (r'^tweets/$',views.getTweets),
    (r'^login/$', views.login_user),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),	
)

