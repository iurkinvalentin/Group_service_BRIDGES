from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'avatar', 'description', 'owner_id', 'members', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Получаем текущего пользователя из контекста
        user_info = self.context['request'].user_info
        validated_data['owner_id'] = user_info['id']  # Используем ID пользователя из auth_service как владельца группы
        return super().create(validated_data)