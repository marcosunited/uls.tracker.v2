from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from mrsauth.views import user, login
from mrsauth.views.AuthorizationViewSets import GroupViewSet, PermissionViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)  # groups url
router.register(r'permissions', PermissionViewSet)  # permissions url

urlpatterns = [
    # Login url
    url(r'^api/v1/login$', login.do_login),

    # User urls
    url(r'^api/v1/user/create$', user.user_init),
    url(r'^api/v1/user$', user.user_list),
    url(r'^api/v1/user/(?P<pk>[0-9]+)$', user.user_detail),
    url(r'^api/v1/user/filter$', user.user_filter),

    # Authentication authorization router managed urls
    url(r'^api/v1/', include(router.urls)),

]
