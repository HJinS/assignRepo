from rest_framework import status
from .serializers import RoutineResultSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import (Prefetch, Q)
from .models import Routine
from routine_result.models import RoutineResult
from routine.response_data_form import ResponseDataForm, ResponseStatusEnum, ResponseMessageEnum


class RoutineResultViewSet(viewsets.ModelViewSet):
    serializer_class = RoutineResultSerializer
    queryset = RoutineResult.objects.all()

    def partial_update(self, request, routine_result_id):
        try:
            routine_result_obj = RoutineResult.objects.get(routine_result_id=routine_result_id)
        except RoutineResult.DoesNotExist:
            return Response("No Data", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(routine_result_obj, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = ResponseDataForm(ResponseStatusEnum.UPDATE_OK, ResponseMessageEnum.MSG_UPDATE).get_response_form()
            response_data['data'] = {
                'routine_result_id': routine_result_obj.routine_result_id
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response("Invalid Data", status=status.HTTP_400_BAD_REQUEST)
