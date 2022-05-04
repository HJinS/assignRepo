from rest_framework import serializers
from .models import Routine
from routine_result.models import RoutineResult
from routine_day.models import RoutineDay


class RoutineSerializer(serializers.ModelSerializer):
    days = serializers.ListSerializer(child=serializers.CharField(max_length=4))

    class Meta:
        fields = '__all__'
        model = Routine

    def create(self, validated_data):
        days = validated_data.pop('days')
        routine = Routine.objects.create(**validated_data)
        RoutineResult.objects.create(routine_id=routine)
        for day in days:
            routine_day = RoutineDay.objects.create(routine_id=routine)
            routine_day.day = day
            routine_day.save()
        return routine

    def update(self, instance, validated_data):
        days = validated_data.get('days', [])
        routine_result = RoutineResult.objects.filter(routine_id=instance)

        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.is_alarm = validated_data.get('is_alarm', instance.is_alarm)
        instance.save()
        if len(routine_result) == 1:
            routine_result[0].result = validated_data.get('result', routine_result[0].result)
            routine_result[0].save()

        if len(days) > 0:
            routine_day = RoutineDay.objects.filter(routine_id=instance)
            for day_obj in routine_day:
                day_obj.delete()
            for day in days:
                new_routine_day = RoutineDay.objects.create(routine_id=instance)
                new_routine_day.day = day
                new_routine_day.save()
        return instance


class RemoveRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('routine_id', 'account_id')
        model = Routine

    def delete(self, instance, validated_data):
        routine_id = validated_data.get('routine_id', instance.routine_id)
        account_id = validated_data.get('account_id', instance.account_id)
        query_set = Routine.objects.filter(routine_id=routine_id, account_id=account_id)
        return query_set.delete()


class GetRoutineListSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField('get_result_prefetch')

    def get_result_prefetch(self, result_obj):
        result = result_obj.routine_result[0].result
        return result

    class Meta:
        fields = ['goal', 'routine_id', 'title', 'result']
        model = Routine


class GetRoutineSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField('get_result_prefetch')
    days = serializers.SerializerMethodField('get_day_prefetch')

    def get_result_prefetch(self, result_obj):
        result = result_obj.routine_result[0].result
        return result

    def get_day_prefetch(self, day_obj):
        day_list = day_obj.days
        days = []
        for day in day_list:
            days.append(day.day)
        return days

    class Meta:
        fields = ['goal', 'routine_id', 'title', 'result', 'days']
        model = Routine
