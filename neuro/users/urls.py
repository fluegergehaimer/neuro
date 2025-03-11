from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserSubscriptionViewSet,
    PremiumContentViewSet,
    MixedContentViewSet
)

app_name = 'users'

router = DefaultRouter()
router.register(r'status', UserSubscriptionViewSet, basename='user-status')
router.register(r'premium', PremiumContentViewSet, basename='premium')
router.register(r'content', MixedContentViewSet, basename='content')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
