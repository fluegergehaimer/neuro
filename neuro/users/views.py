from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsPaidSubscriber
from .models import NeuroUser

class UserIsPaidViewSet(viewsets.ViewSet):
    def list(self, request):
        users = NeuroUser.objects.all()
        return Response([{'id': user.id, 'is_paid': user.is_paid()} for user in users])

    def retrieve(self, request, pk=None):
        try:
            user = NeuroUser.objects.get(pk=pk)
            return Response({'id': user.id, 'is_paid': user.is_paid()})
        except NeuroUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def toggle_paid_status(self, request, pk=None):
        try:
            user = NeuroUser.objects.get(pk=pk)
            user.is_paid_subscriber = not user.is_paid_subscriber
            user.save()
            return Response({
                'id': user.id,
                'is_paid': user.is_paid(),
                'message': 'Статус подписки успешно изменен'
            })
        except NeuroUser.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

class PremiumContentViewSet(viewsets.ViewSet):
    permission_classes = [IsPaidSubscriber]

    def list(self, request):
        return Response({'message': 'Это премиум контент'})

class MixedContentViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['free_content', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsPaidSubscriber]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return Response({'message': 'Базовый контент'})

    @action(detail=False, methods=['get'])
    def free_content(self, request):
        return Response({'message': 'Бесплатный контент'})

    @action(detail=False, methods=['get'])
    def premium_content(self, request):
        return Response({'message': 'Премиум контент'})