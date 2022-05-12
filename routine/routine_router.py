from rest_framework.routers import DefaultRouter, Route


class RoutineRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'patch': 'partial_update',
                'delete': 'destroy'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'List'}
        )
    ]
