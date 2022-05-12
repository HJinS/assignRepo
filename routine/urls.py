from django.urls import path, include
from .routine_router import RoutineRouter
from . import views

router = RoutineRouter()
router.register(r'routines', views.RoutineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
