from rest_framework import serializers
from .models import RoutineDay


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = RoutineDay

    def validate_day(self, value):
        if value not in ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'):
            raise serializers.ValidationError('This is not a day')
        return value

    def create(self, validated_data):
        routine_day = RoutineDay.objects.create(**validated_data)
        return routine_day
