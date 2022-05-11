from __future__ import absolute_import
from djangoProject.celery import app
from routine_day.models import RoutineDay
from routine_result.serializers import RoutineResultSerializer
from datetime import datetime, timedelta
from pytz import timezone


@app.task(bind=True)
def make_results_task():
    today = datetime.today(timezone('Asia/Seoul'))
    today_day = today.weekday()
    routine_day = RoutineDay.objects.filter(day=today_day).select_related('routine_id')
    for routine_item in routine_day:
        routine_id = routine_item.routine_id.routine_id
        new_routine_result = RoutineResultSerializer(data={'routine_id': routine_id, 'created_at': today+timedelta(days=7), 'modified_at': today})
        if new_routine_result.is_valid(raise_exception=True):    
            new_routine_result.save()
