from django.urls import path
from . import views


urlpatterns = [
    path('createRoutine', views.CreateRoutineView.as_view()),
    path('updateRoutine', views.UpdateRoutineView.as_view()),
    path('getRoutine', views.GetRoutineView.as_view()),
    path('getRoutineList', views.GetRoutineListView.as_view()),
    path('deleteRoutine', views.DeleteRoutineView.as_view()),
]