from django.urls import path, include
from .routine_result_router import RoutineResultRouter
from . import views

router = RoutineResultRouter()
router.register(r'routine-results', views.RoutineResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
