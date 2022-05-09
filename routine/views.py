from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoutineSerializer, GetRoutineSerializer, GetRoutineListSerializer
from rest_framework.response import Response
from django.db.models import (Prefetch, Q)

from .models import Routine
from routine_result.models import RoutineResult


class CreateRoutineView(APIView):

    def post(self, request):
        data = request.data.copy()
        data.update({'account_id': request.user.id})
        serializer = RoutineSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            routine = serializer.save()
            return_data = {
                "data": {
                    "routine_id": routine.routine_id
                },
                "message": {
                    "msg": "루틴 생성 성공", "status": "ROUTINE_CREATE_OK"
                }
            }
            return Response(return_data, status=status.HTTP_201_CREATED)
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class GetRoutineListView(APIView):

    def post(self, request):
        account_id = request.data['account_id']
        created_at = request.data['today']
        query_set = RoutineResult.objects.filter(created_at=created_at).select_related('routine_id').filter(routine_id__account_id=account_id)

        serializer = GetRoutineListSerializer(query_set, many=True)
        return_data = {
            "data": serializer.data,
            "message": {
                "msg": "루틴 조회 성공", "status": "ROUTINE_LIST_OK"
            }
        }
        return Response(return_data, status=status.HTTP_200_OK)


class GetRoutineView(APIView):

    def post(self, request):
        try:
            account_id = request.data['account_id']
            routine_id = request.data['routine_id']
        except Exception:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
        filter_q = Q()
        filter_q &= Q(routine_id__account_id=account_id)
        filter_q &= Q(routine_id=routine_id)
        query_set = RoutineResult.objects.select_related('routine_id').filter(filter_q).prefetch_related(Prefetch('routine_id__routine_day_relate', to_attr='routine_day_res'))
        serializer = GetRoutineSerializer(query_set, many=True)
        try:
            serialized_data = serializer.data[0]
        except:
            serialized_data = []
        return_data = {
            "data": serialized_data,
            "message": {
                "msg": "루틴 조회 성공", "status": "ROUTINE_DETAIL_OK"
            }
        }
        return Response(return_data, status=status.HTTP_200_OK)


class UpdateRoutineView(APIView):

    def post(self, request):
        routine_id = request.data['routine_id']
        account_id = request.user.id
        try:
            routine_obj = Routine.objects.get(routine_id=routine_id, account_id=account_id)
        except Routine.DoesNotExist:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
        serializer = RoutineSerializer(routine_obj, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return_data = {
                "data": {
                    "routine_id": routine_id
                },
                "message": {
                    "msg": "루틴 수정 성공", "status": "ROUTINE_UPDATE_OK"
                }
            }
            return Response(return_data, status=status.HTTP_200_OK)
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class DeleteRoutineView(APIView):

    def post(self, request):
        try:
            routine_id = request.data['routine_id']
            account_id = request.data['account_id']
            routine = Routine.objects.get(routine_id=routine_id, account_id=account_id)
            routine.delete()
            return_data = {
                "data": {
                    "routine_id": routine_id
                },
                "message": {
                    "msg": "루틴 삭제 성공", "status": "ROUTINE_DELETE_OK"
                }
            }
            return Response(return_data, status=status.HTTP_200_OK)
        except Routine.DoesNotExist:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)



