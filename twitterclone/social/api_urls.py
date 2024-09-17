from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, TweetViewSet, RegisterView, LoginAPIView, FeedAPIView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'tweets', TweetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('feed/', FeedAPIView.as_view(), name='api-feed'),
]