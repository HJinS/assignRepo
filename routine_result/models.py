from django.db import models
from routine.models import Routine
import uuid


class RoutineResult(models.Model):
    RESULTS = (
        ('N', 'NOT'),
        ('T', 'TRY'),
        ('D', 'DONE')
    )
    routine_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='routine_result_relate')
    result = models.CharField(max_length=1, choices=RESULTS, default="N")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
