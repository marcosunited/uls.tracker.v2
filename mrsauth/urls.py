from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from mrsauth.views import UserViewSet, login
from mrsauth.views.AuthorizationViewSets import *

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'permissions', PermissionViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    # Login url
    url(r'^api/v1/login$', login.do_login),

    # User urls
    url(r'^api/v1/user/create$', UserViewSet.UserInit.as_view()),
    url(r'^api/v1/user$', UserViewSet.UserList.as_view()),
    url(r'^api/v1/user/(?P<pk>[0-9]+)$', UserViewSet.UserDetail.as_view()),
    url(r'^api/v1/user/filter$', UserViewSet.UserFilter.as_view()),

    # Authentication-authorization router managed urls
    url(r'^api/v1/', include(router.urls)),

]
