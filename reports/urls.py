from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    get_current_user, 
    user_list_create, 
    user_detail_update_delete,
    department_list_create,
    report_list_create, 
    report_update_delete, 
    add_comment
)

urlpatterns = [
    # JWT Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Endpoints
    path('auth/me/', get_current_user, name='get_current_user'),
    path('users/', user_list_create, name='user_list_create'),
    path('users/<int:pk>/', user_detail_update_delete, name='user_detail_update_delete'),

    # Department Endpoints
    path('departments/', department_list_create, name='department_list_create'),

    # Report Endpoints
    path('reports/', report_list_create, name='report_list_create'),
    path('reports/<int:pk>/', report_update_delete, name='report_update_delete'),

    # Comment Endpoint
    path('reports/<int:report_id>/comment/', add_comment, name='add_comment'),
]

