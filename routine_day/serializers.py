from rest_framework import serializers
from .models import RoutineDay


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = RoutineDay

    def create(self, validated_data):
        routine_day = RoutineDay.objects.create(**validated_data)
        return routine_day
