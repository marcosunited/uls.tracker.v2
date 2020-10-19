from django.conf.urls import url
from mrsauth.views import *

urlpatterns = [
    # Login url
    url(r'^api/v1/login$', login.do_login),

    #Create user url
    url(r'^api/v1/user/create$', user.user_init),

    #User urls
    url(r'^api/v1/user$', user.user_list),
    url(r'^api/v1/user/(?P<pk>[0-9]+)$', user.user_detail),
    url(r'^api/v1/user/filter$', user.user_filter),
]
