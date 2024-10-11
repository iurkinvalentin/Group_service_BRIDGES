from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, GroupCreateView
from django.urls import path

# Настройка маршрутизатора
router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups')

# Дополнительные маршруты
urlpatterns = [
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
]

# Объединяем маршруты маршрутизатора и дополнительные пути
urlpatterns += router.urls