from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

from mrsauth.views import UserViewSet, login, AuthorizationViewSets
from mrsauth.views.AuthorizationViewSets import *

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'permissions', PermissionViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    # Login url
    url(r'^api/v1/login$', login.do_login),

    # Logout url
    url(r'^api/v1/logout$', login.do_logout),

    # Refresh token
    url(r'^api/v1/token-refresh$', refresh_jwt_token),

    # User urls
    url(r'^api/v1/user/create$', UserViewSet.UserInit.as_view()),
    url(r'^api/v1/user$', UserViewSet.UserList.as_view()),
    url(r'^api/v1/user/(?P<pk>[0-9]+)$', UserViewSet.UserDetail.as_view()),
    url(r'^api/v1/user/filter$', UserViewSet.UserFilter.as_view()),

    # Group - User
    url(r'^api/v1/group/(?P<pk_group>[0-9]+)/user/(?P<pk_user>[0-9]+)$', AuthorizationViewSets.GroupUserRelationView.as_view()),

    # Authentication-authorization router managed urls
    url(r'^api/v1/', include(router.urls)),

]
