from django.urls import path, include
from education.apps import EducationConfig

from rest_framework.routers import DefaultRouter

from education.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateView, PaymentListAPIView, SubscribeCreateAPIView, \
    SubscribeUpdateAPIView, SubscribeDeleteAPIView

app_name = EducationConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),

    path('users/', include('users.urls', namespace='users')),

    path('course/<int:pk>/subscribe/', SubscribeCreateAPIView.as_view(), name='subscribe_create'),
    path('course/subscribe/update/<int:pk>/', SubscribeUpdateAPIView.as_view(), name='subscribe_update'),
    path('course/subscribe/delete/<int:pk>/', SubscribeDeleteAPIView.as_view(), name='subscribe_delete'),
] + router.urls
