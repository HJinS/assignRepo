from django.db import models
from routine.models import Routine


class RoutineDay(models.Model):
    day = models.CharField(max_length=4)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='routine_day_relate')
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
