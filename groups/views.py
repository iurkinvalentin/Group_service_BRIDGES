from rest_framework import viewsets
from .models import Group
from .serializers import GroupSerializer
from rest_framework.response import Response
from .utils import get_user_info


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        group = self.get_object()
        owner_info = get_user_info(group.owner_id)  # Получаем данные о владельце группы
        members_info = [get_user_info(member_id) for member_id in group.members]  # Получаем данные об участниках

        # Формируем ответ с полной информацией о группе, владельце и участниках
        group_data = {
            "group": GroupSerializer(group).data,
            "owner": owner_info,
            "members": members_info,
        }
        return Response(group_data)
