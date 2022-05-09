from django.db import models
from routine.models import Routine
import uuid


class RoutineResult(models.Model):
    routine_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='routine_result_relate')
    result = models.CharField(max_length=4, default='NOT')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
