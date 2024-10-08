from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'avatar', 'description', 'owner_id', 'members', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']