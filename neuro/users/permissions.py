from rest_framework import permissions

class HasSubscriptionPermission(permissions.BasePermission):
    message = 'У вас нет доступа к этому контенту. Требуется подписка.'

    def has_object_permission(self, request, view, obj):
        # obj может быть постом или другим контентом с required_subscription
        return request.user.is_authenticated and request.user.has_access_to_subscription(obj.required_subscription) 