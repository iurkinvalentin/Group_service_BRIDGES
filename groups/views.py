from rest_framework import viewsets
from .models import Group
from .serializers import GroupSerializer
from rest_framework.response import Response
from .utils import get_user_info
import logging
from rest_framework import permissions


class GroupViewSet(viewsets.ViewSet):
    """Унифицированное представление для работы с группами"""
    queryset = Group.objects.all()  # Добавляем атрибут queryset
    serializer_class = GroupSerializer

    def list(self, request):
        # Извлекаем заголовок Authorization
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        print(token)
        # Логика работы с токеном
        user_data = get_user_info(token)
        # Продолжение логики
        return Response({"message": "Запрос успешно обработан", "user": user_data})
