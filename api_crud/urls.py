
from django.contrib import admin
from django.conf.urls import include, url
from .views import RegisterView, CustomLoginView
from rest_framework.routers import DefaultRouter
from order.views import *
from django.urls import path, include
# from rest_

router_v1 = DefaultRouter()
router_v1.register('order', OrderViewSet, basename='order')

# urls
urlpatterns = [
    # url(r'^', include('movies.urls')),
    url(r'^rest-auth/login/', CustomLoginView.as_view()),
    url(r'^rest-auth/registration/', RegisterView.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^admin/', admin.site.urls),
    path(r'v1/', include(router_v1.urls))
]