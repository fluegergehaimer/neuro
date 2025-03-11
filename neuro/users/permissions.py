from rest_framework import permissions

class IsPaidSubscriber(permissions.BasePermission):
    """
    Пользовательское разрешение для проверки статуса подписки.
    """
    message = 'Этот контент доступен только для платных подписчиков.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_paid() 