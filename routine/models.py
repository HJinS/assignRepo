from django.db import models
import uuid
from user.models import RoutineUser


class Routine(models.Model):
    routine_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account_id = models.ForeignKey(RoutineUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=10)
    goal = models.CharField(max_length=50)
    is_alarm = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
