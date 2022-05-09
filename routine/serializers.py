from rest_framework import serializers
from .models import Routine
from routine_result.models import RoutineResult
from routine_day.models import RoutineDay
from routine_day.serializers import RoutineDaySerializer
from routine_result.serializers import RoutineResultSerializer


class RoutineSerializer(serializers.ModelSerializer):
    days = serializers.ListSerializer(child=serializers.CharField(max_length=4))

    class Meta:
        fields = '__all__'
        model = Routine

    def validate_category(self, value):
        if value not in ('HOMEWORK', 'MIRACLE'):
            raise serializers.ValidationError("This field must be HOMEWORK or MIRACLE")
        return value

    def validate_days(self, value):
        value_set = set(value)
        if not value_set & {'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'} == value_set:
            raise serializers.ValidationError("This is not a day")
        if not value:
            raise serializers.ValidationError("Day is required")
        return value

    def create(self, validated_data):
        if validated_data['category'] not in ('HOMEWORK', 'MIRACLE'):
            self.fail('Invalid data')
        days = validated_data.pop('days')
        routine = Routine.objects.create(**validated_data)
        routine_result = RoutineResultSerializer(data={'routine_id': routine.routine_id, 'days': days})
        if routine_result.is_valid(raise_exception=True):
            routine_result.save()
        for day in days:
            routine_day = RoutineDaySerializer(data={'routine_id': routine.routine_id, 'day': day})
            if not routine_day.is_valid(raise_exception=True):
                raise serializers.ValidationError("Invalid data")
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
            routine_day = RoutineDay.objects.filter(routine_id=instance)
            for day_obj in routine_day:
                day_obj.delete()
            for day in days:
                new_routine_day = RoutineDay.objects.create(routine_id=instance)
                new_routine_day.day = day
                new_routine_day.save()
        return instance


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


class GetRoutineSerializer(serializers.ModelSerializer):
    goal = serializers.SerializerMethodField('get_result_goal')
    title = serializers.SerializerMethodField('get_result_title')
    days = serializers.SerializerMethodField('get_day_prefetch')

    def get_result_goal(self, result_obj):
        return result_obj.routine_id.goal

    def get_result_title(self, result_obj):
        return result_obj.routine_id.title

    def get_day_prefetch(self, day_obj):
        day_list = day_obj.routine_id.routine_day_res
        days = []
        for day in day_list:
            days.append(day.day)
        return days

    class Meta:
        fields = ['result', 'goal', 'routine_id', 'title', 'days']
        model = RoutineResult
