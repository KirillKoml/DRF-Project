from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserUpdateAPIView, UserRetrieveAPIView, UserDestroyAPIView, \
    PaymentListAPIView, PaymentCreateAPIView, PaymentStatusRetrieveView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/<int:pk>/retrieve/', UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('user/<int:pk>/destroy/', UserDestroyAPIView.as_view(), name='user-destroy'),

    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/<int:pk>/status/', PaymentStatusRetrieveView.as_view(), name='payment-status'),
]