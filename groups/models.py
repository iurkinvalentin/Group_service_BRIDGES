from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    description = models.TextField(blank=True)
    owner_id = models.IntegerField()  # Храним ID владельца, полученного из auth_service
    members = models.JSONField(default=list)  # Храним список ID участников группы
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
