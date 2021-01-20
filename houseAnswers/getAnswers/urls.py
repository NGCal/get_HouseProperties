from rest_framework import routers
from django.urls import path, include
from .api import ResponseViewSet


urlpatterns = [path('api/answers', ResponseViewSet.as_view())]
