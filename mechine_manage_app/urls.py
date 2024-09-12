from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, RegisterView,AxisViewSet,MachineViewSetForSingleData, ToolsInUseViewSet,MachineHistoricalDataView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('machines/<str:machine_id>/', MachineViewSetForSingleData.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='machine-detail'),
    path('machines/', MachineViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='machine-list'),
    path('toolsinuse/<str:machine_id>/', ToolsInUseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='toolsinuse-detail'),

    path('toolsinuse/', ToolsInUseViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='toolsinuse-list'),
    path('machine/historical-data/', MachineHistoricalDataView.as_view(), name='machine-historical-data'),
    path('axes/<str:machine_id>/<str:axis_name>/', AxisViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='axis-detail'),
    path('axes/<str:machine_id>/', AxisViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='axis-list'),

]
