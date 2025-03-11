from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet

app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

# Вложенные маршруты для комментариев и лайков
posts_router = DefaultRouter()
posts_router.register(r'comments', CommentViewSet, basename='comments')
posts_router.register(r'likes', LikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/', include(posts_router.urls)),
] 