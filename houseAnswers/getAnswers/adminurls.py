from rest_framework import routers
from django.urls import path, include
from .api import ProviderViewSet, FieldsViewSet

router = routers.DefaultRouter()
router.register("api/provider", ProviderViewSet,"provider")
router.register("api/fields", FieldsViewSet,"fields")


urlpatterns = router.urls
