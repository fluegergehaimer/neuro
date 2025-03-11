from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_password_length(value):
    if len(value) > 20:
        raise ValidationError(
            'Пароль не должен превышать 20 символов',
            code='password_too_long'
        )

class SubscriptionType(models.Model):
    """Модель типа подписки"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    includes_subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='included_in',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип подписки'
        verbose_name_plural = 'Типы подписок'

    def __str__(self):
        return self.name

class NeuroUser(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=20,
        unique=True,
        # validators=[validate_username, validate_username_via_regex]
    )
    password = models.CharField(
        max_length=128,  # Стандартная длина для хешированных паролей в Django
        verbose_name='Пароль'
    )
    email = models.EmailField(
        max_length=30,
        verbose_name='Адрес электронной почты',
        unique=True)
    first_name = models.CharField(
        max_length=20,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия'
    )

    subscription = models.ForeignKey(
        SubscriptionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscribers'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:20]
    
    def has_access_to_subscription(self, subscription_type):
        """Проверяет, есть ли у пользователя доступ к определенному типу подписки"""
        if not self.subscription:
            return False
        if self.subscription == subscription_type:
            return True
        return subscription_type in self.subscription.includes_subscriptions.all()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        if raw_password:
            validate_password_length(raw_password)
        super().set_password(raw_password)
    


