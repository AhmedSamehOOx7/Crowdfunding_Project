from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CategoryListAPIView, CampaignViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
]
