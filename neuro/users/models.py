from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_password_length(value):
    if len(value) > 20:
        raise ValidationError(
            'Пароль не должен превышать 20 символов',
            code='password_too_long'
        )

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

    is_paid_subscriber = models.BooleanField(
        verbose_name='Платный подписчик',
        default=False
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:20]
    
    def is_paid(self):
        return self.is_paid_subscriber
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        if raw_password:
            validate_password_length(raw_password)
        super().set_password(raw_password)
    


