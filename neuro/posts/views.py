from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import HasSubscriptionPermission
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, HasSubscriptionPermission]

    def get_queryset(self):
        user = self.request.user
        if user.subscription:
            # Получаем все типы подписок, к которым у пользователя есть доступ
            accessible_subscriptions = [user.subscription]
            accessible_subscriptions.extend(user.subscription.includes_subscriptions.all())
            return Post.objects.filter(required_subscription__in=accessible_subscriptions)
        return Post.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Для всех авторизованных пользователей

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(post_id=self.kwargs.get('post_id'))

    @action(detail=False, methods=['post'])
    def toggle(self, request, post_id=None):
        try:
            post = Post.objects.get(id=post_id)
            like, created = Like.objects.get_or_create(
                user=request.user,
                post=post
            )
            if not created:
                like.delete()
                return Response({'status': 'unliked'})
            return Response({'status': 'liked'})
        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
