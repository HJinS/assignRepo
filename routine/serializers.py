from rest_framework import serializers
from .models import Routine
from routine_result.models import RoutineResult
from routine_day.models import RoutineDay
from routine_day.serializers import RoutineDaySerializer
from routine_result.serializers import RoutineResultSerializer
from datetime import datetime, timedelta
from pytz import timezone


class RoutineSerializer(serializers.ModelSerializer):
    days = serializers.ListSerializer(child=serializers.CharField(max_length=4))

    class Meta:
        fields = '__all__'
        model = Routine

    def validate_category(self, value):
        if value not in ('HOMEWORK', 'MIRACLE'):
            raise serializers.ValidationError('This field must be HOMEWORK or MIRACLE')
        return value

    def validate_days(self, value):
        value_set = set(value)
        if not value:
            raise serializers.ValidationError('Day is required')
        if not value_set & {'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'} == value_set:
            raise serializers.ValidationError('This is not a day')
        return value

    def create(self, validated_data):
        days = validated_data.pop('days')
        routine = Routine.objects.create(**validated_data)
        routine_result = RoutineResultSerializer(data={'routine_id': routine.routine_id, 'days': days})
        if routine_result.is_valid(raise_exception=True):
            routine_result.save()
        for day in days:
            routine_day = RoutineDaySerializer(data={'routine_id': routine.routine_id, 'day': day})
            if not routine_day.is_valid(raise_exception=True):
                print("check_serializer")
                raise serializers.ValidationError('Invalid data')
            routine_day.save()
        return routine

    def update(self, instance, validated_data):
        days = validated_data.get('days', [])
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.is_alarm = validated_data.get('is_alarm', instance.is_alarm)
        instance.save()
        if len(days) > 0:
            self.update_days(instance, days)
            self.update_results(instance, days)
        return instance

    def update_days(self, instance, days):
        routine_day = RoutineDay.objects.filter(routine_id=instance)
        for day_obj in routine_day:
            day_obj.delete()
        for day in days:
            new_routine_day = RoutineDay.objects.create(routine_id=instance)
            new_routine_day.day = day
            new_routine_day.save()

    def update_results(self, instance, days):
        day_to_int = {
            'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6
        }
        today = datetime.now(timezone('Asia/Seoul'))
        today_day = today.weekday()
        start_of_week = today + timedelta(days=(-today_day + 7))
        end_of_week = start_of_week + timedelta(days=(6 + 7))
        routine_result = RoutineResult.objects.filter(routine_id=instance, created_at__range=[start_of_week, end_of_week])
        if len(routine_result) > 0:
            routine_result.delete()
        for day in days:
            routine_result_date = start_of_week + timedelta(day_to_int[day])
            data = {
                'routine_id': instance.routine_id,
                'created_at': routine_result_date.strftime('%Y-%m-%d'),
                'modified_at': routine_result_date.strftime('%Y-%m-%d')
            }
            new_routine_result = RoutineResultSerializer(data=data)
            if new_routine_result.is_valid(raise_exception=True):
                new_routine_result.save()


class GetRoutineListSerializer(serializers.ModelSerializer):
    goal = serializers.SerializerMethodField('get_result_goal')
    title = serializers.SerializerMethodField('get_result_title')

    def get_result_goal(self, result_obj):
        return result_obj.routine_id.goal

    def get_result_title(self, result_obj):
        return result_obj.routine_id.title

    class Meta:
        fields = ['result', 'goal', 'routine_id', 'title']
        model = RoutineResult


class GetRoutineSerializer(GetRoutineListSerializer):
    days = serializers.SerializerMethodField('get_day_prefetch')

    def get_day_prefetch(self, day_obj):
        day_list = day_obj.routine_id.routine_day_res
        days = []
        for day in day_list:
            days.append(day.day)
        return days

    class Meta:
        fields = ['result', 'goal', 'routine_id', 'title', 'days']
        model = RoutineResult
