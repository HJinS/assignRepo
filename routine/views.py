import datetime

import pytz
from rest_framework import status
from .serializers import RoutineSerializer, GetRoutineSerializer, GetRoutineListSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import (Prefetch, Q)
from .models import Routine
from routine_result.models import RoutineResult
from .response_data_form import ResponseDataForm, ResponseMessageEnum, ResponseStatusEnum


class RoutineViewSet(viewsets.ModelViewSet):
    serializer_class = RoutineSerializer
    queryset = Routine.objects.all()
    lookup_field = None

    def create(self, request):
        request_data = request.data.copy()
        request_data.update({'account_id': request.user.id})
        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            routine = serializer.save()
            return_data = ResponseDataForm(ResponseStatusEnum.CREATE_OK, ResponseMessageEnum.MSG_CREATE).form
            return_data['data'] = {
                'routine_id': routine.routine_id
            }
            return Response(return_data, status=status.HTTP_201_CREATED)
        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request):
        account_id = request.user.id
        routine_id = request.query_params.get('routine_id')
        try:
            routine_obj = Routine.objects.get(routine_id=routine_id, account_id=account_id)
        except Routine.DoesNotExist:
            return Response('No data', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(routine_obj, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return_data = ResponseDataForm(ResponseStatusEnum.UPDATE_OK, ResponseMessageEnum.MSG_UPDATE).form
            return_data['data'] = {
                'routine_id': routine_id
            }
            return Response(return_data, status=status.HTTP_200_OK)
        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        try:
            account_id = request.user.id
            routine_id = request.query_params.get('routine_id')
            routine = Routine.objects.get(routine_id=routine_id, account_id=account_id)
            routine.delete()
            return_data = ResponseDataForm(ResponseStatusEnum.DELETE_OK, ResponseMessageEnum.MSG_DELETE).form
            return_data['data'] = {
                'routine_id': routine_id
            }
            return Response(return_data, status=status.HTTP_200_OK)
        except Routine.DoesNotExist:
            return Response('No data', status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    def routine_list(self, account_id, today):
        current_day = datetime.datetime.now(pytz.timezone('Asia/Seoul')).today()
        today_obj = datetime.datetime.fromisoformat(today)
        if current_day < today_obj:
            return Response("Can't get future's result", status=status.HTTP_400_BAD_REQUEST)
        query_set = RoutineResult.objects.filter(created_at=today).select_related('routine_id').filter(routine_id__account_id=account_id)
        serializer = GetRoutineListSerializer(query_set, many=True)
        return_data = ResponseDataForm(ResponseStatusEnum.LIST_OK, ResponseMessageEnum.MSG_LIST).form
        return_data['data'] = serializer.data
        return Response(return_data, status=status.HTTP_200_OK)

    def routine_get(self, account_id, routine_id):
        try:
            filter_q = Q()
            filter_q &= Q(routine_id__account_id=account_id)
            filter_q &= Q(routine_id=routine_id)
            query_set = RoutineResult.objects.select_related('routine_id').filter(filter_q).prefetch_related(Prefetch('routine_id__routine_day_relate', to_attr='routine_day_res'))
            serializer = GetRoutineSerializer(query_set[0], many=False)
            return_data = ResponseDataForm(ResponseStatusEnum.DETAIL_OK, ResponseMessageEnum.MSG_DETAIL).form
            serialized_data = serializer.data
            return_data['data'] = serialized_data
            return Response(return_data, status=status.HTTP_200_OK)
        except Routine.DoesNotExist:
            return Response('No data', status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        account_id = request.user.id
        query_param = request.query_params
        today = query_param.get('today')
        routine_id = query_param.get('routine_id')
        if today:
            response = self.routine_list(account_id, today)
            return response
        else:
            response = self.routine_get(account_id, routine_id)
            return response
