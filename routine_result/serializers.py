from rest_framework import serializers
from .models import RoutineResult


class RoutineResultSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'result'
        model = RoutineResult

    def create(self, validated_data):
        routine_result_data = RoutineResult.objects.create(**validated_data)
        return routine_result_data
