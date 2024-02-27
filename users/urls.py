from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UserCreateAPIView, UserRetrieveAPIView

app_name = 'users'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserCreateAPIView.as_view(), name='user_update'),
]
