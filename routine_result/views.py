from rest_framework import status
from .serializers import RoutineResultSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from routine_result.models import RoutineResult
from routine.response_data_form import ResponseDataForm, ResponseStatusEnum, ResponseMessageEnum


class RoutineResultViewSet(viewsets.ModelViewSet):
    serializer_class = RoutineResultSerializer
    queryset = RoutineResult.objects.all()

    def partial_update(self, request):
        routine_result_id = request.query_params.get('routine_result_id')
        account_id = request.user.id
        if not routine_result_id:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
        try:
            routine_result_obj = RoutineResult.objects.get(routine_result_id=routine_result_id, routine_id__account_id=account_id)
            serializer = self.get_serializer(routine_result_obj, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data = ResponseDataForm(ResponseStatusEnum.UPDATE_OK, ResponseMessageEnum.MSG_UPDATE).form
                response_data['data'] = {
                    'routine_result_id': routine_result_obj.routine_result_id
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except RoutineResult.DoesNotExist:
            return Response("No data", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
