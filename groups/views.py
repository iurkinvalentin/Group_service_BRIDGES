from rest_framework import viewsets
from .models import Group
from .serializers import GroupSerializer
from rest_framework.response import Response
from .utils import get_user_info
import logging
from rest_framework import permissions
from rest_framework import generics, status
from rest_framework.views import APIView


class GroupViewSet(viewsets.ViewSet):
    """Унифицированное представление для работы с группами"""
    queryset = Group.objects.all()  # Добавляем атрибут queryset
    serializer_class = GroupSerializer

    def list(self, request):
        # Извлекаем заголовок Authorization
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        print(auth_header)
        print(token)
        # Логика работы с токеном
        user_data = get_user_info(token)
        print(user_data)
        # Продолжение логики
        return Response({"message": "Запрос успешно обработан", "user": user_data})


class GroupCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def post(self, request, *args, **kwargs):
        # Проверяем, что пользователь прошел аутентификацию через middleware
        if not request.user_info:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Переопределяем метод post для добавления данных пользователя в контекст
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()

        # Возвращаем информацию о группе и пользователе
        return Response({
            'group': GroupSerializer(group).data,
            'user': request.user_info
        }, status=status.HTTP_201_CREATED)






