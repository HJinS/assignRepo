from rest_framework.routers import DefaultRouter, Route


class RoutineResultRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'patch': 'partial_update'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'Partial Update'}
        )
    ]
