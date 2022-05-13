from __future__ import absolute_import
from djangoProject.celery import app
from routine_day.models import RoutineDay
from routine_result.serializers import RoutineResultSerializer
from datetime import datetime, timedelta
from pytz import timezone


@app.task
def make_results_task():
    int_to_day = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    now = datetime.now(timezone('Asia/Seoul'))
    today = now.today()
    today_day = today.weekday()
    routine_day = RoutineDay.objects.filter(day=int_to_day[today_day]).select_related('routine_id')
    next_day = today + timedelta(days=7)
    for routine_item in routine_day:
        routine_id = routine_item.routine_id.routine_id
        new_routine_result = RoutineResultSerializer(data={'routine_id': routine_id, 'created_at': next_day.strftime('%Y-%m-%d'), 'modified_at': next_day.strftime('%Y-%m-%d')})
        if new_routine_result.is_valid(raise_exception=True):    
            new_routine_result.save()
