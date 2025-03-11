from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import HasSubscriptionPermission
from .models import NeuroUser, SubscriptionType

class UserSubscriptionViewSet(viewsets.ViewSet):
    def list(self, request):
        users = NeuroUser.objects.all()
        return Response([{
            'id': user.id,
            'subscription': user.subscription.name if user.subscription else None
        } for user in users])

    def retrieve(self, request, pk=None):
        try:
            user = NeuroUser.objects.get(pk=pk)
            return Response({
                'id': user.id,
                'subscription': user.subscription.name if user.subscription else None
            })
        except NeuroUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def change_subscription(self, request, pk=None):
        try:
            user = NeuroUser.objects.get(pk=pk)
            subscription_id = request.data.get('subscription')
            
            if subscription_id:
                try:
                    subscription = SubscriptionType.objects.get(pk=subscription_id)
                    user.subscription = subscription
                    user.save()
                except SubscriptionType.DoesNotExist:
                    return Response(
                        {'error': 'Подписка не найдена'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                user.subscription = None
                user.save()

            return Response({
                'id': user.id,
                'subscription': user.subscription.name if user.subscription else None,
                'message': 'Подписка успешно изменена'
            })
        except NeuroUser.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

class PremiumContentViewSet(viewsets.ViewSet):
    permission_classes = [HasSubscriptionPermission]

    def list(self, request):
        return Response({'message': 'Это премиум контент'})

class MixedContentViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['free_content', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [HasSubscriptionPermission]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return Response({'message': 'Базовый контент'})

    @action(detail=False, methods=['get'])
    def free_content(self, request):
        return Response({'message': 'Бесплатный контент'})

    @action(detail=False, methods=['get'])
    def premium_content(self, request):
        return Response({'message': 'Премиум контент'})