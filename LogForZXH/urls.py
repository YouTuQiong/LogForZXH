

from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from ZXH.views import *
router = routers.DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'Log',LogViewSet)
#router.register(r'fuck',LogView.as_view())
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^register', UserRegisterAPIView.as_view()),
    url(r'^login', UserLoginAPIView.as_view()),
    url(r'^logOut$', LogoutAPIView.as_view()),
    url(r'^fuck/(?P<pk>[0-9]+)/$', LogView.as_view()),
    # url(r'^Logs/', LogViewSet.as_view({'get': 'list'}))
]
