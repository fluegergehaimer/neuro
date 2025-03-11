from django.db import models
from django.conf import settings
from users.models import SubscriptionType


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    required_subscription = models.ForeignKey(
        SubscriptionType,
        on_delete=models.PROTECT,
        related_name='posts'
    )

    def __str__(self):
        return self.title[:20]
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title[:20]} - {self.text[:20]}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f'{self.post.title[:20]} - {self.user.username[:20]}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


