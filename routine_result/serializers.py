from rest_framework import serializers
from .models import RoutineResult
from datetime import datetime, timedelta


class RoutineResultSerializer(serializers.ModelSerializer):
    days = serializers.ListSerializer(child=serializers.CharField(max_length=4), required=False)
    created_at = serializers.DateField(required=False)
    modified_at = serializers.DateField(required=False)

    class Meta:
        fields = '__all__'
        model = RoutineResult

    def validate_result(self, value):
        if value not in ('NOT', 'TRY', 'DONE'):
            raise serializers.ValidationError('This field must be NOT or TRY or DONE')
        return value

    def validate_days(self, value):
        value_set = set(value)
        if not value_set & {'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'} == value_set:
            raise serializers.ValidationError('This is not a day')
        return value

    def create(self, validated_data):
        day_to_int = {
            'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6
        }
        routine_id = validated_data['routine_id']
        try:
            days = validated_data['days']
        except:
            routine_result = RoutineResult.objects.create(**validated_data)
            return routine_result
        result_list = []
        for day in days:
            today = datetime.today().weekday()
            day_int = day_to_int[day]
            diff = day_int - today
            if diff >= 0:
                time_delta = timedelta(days=diff)
                routine_result_time = (datetime.today() + time_delta).strftime('%Y-%m-%d')
                routine_result = RoutineResult(routine_id=routine_id, created_at=routine_result_time, modified_at=routine_result_time)
                routine_result.save()
                result_list.append(routine_result)
        return result_list

    def update(self, instance, validated_data):
        result = validated_data['result']
        instance.result = result
        instance.save()
        return instance

