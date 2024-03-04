from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson, Payment, Subscribe
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import Moderator, Author
from education.tasks import send_updates


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        permission_classes = (IsAuthenticated, Author)
        if self.action == 'create':
            permission_classes = (IsAuthenticated, ~Moderator)
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = (IsAuthenticated, Moderator | Author)
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = (IsAuthenticated, Author | Moderator)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.author = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        send_updates.delay(course.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~Moderator,)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.author = self.request.user
        new_lesson.save()
        send_updates.delay(new_lesson.course.pk)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, Author | Moderator,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, Author | Moderator,)

    def perform_update(self, serializer):
        lesson = serializer.save()
        send_updates.delay(lesson.course.pk)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, Author,)


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)

class SubscribeCreateAPIView(generics.CreateAPIView):
    """Создание подписки на курс"""
    serializer_class = SubscriptionSerializer
    queryset = Subscribe.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        new_subscribe = serializer.save()
        new_subscribe.user = self.request.user
        new_subscribe.course = Course.objects.get(pk=self.kwargs.get('pk'))
        new_subscribe.is_subscribe = True
        new_subscribe.save()


class SubscribeUpdateAPIView(generics.UpdateAPIView):
    """Редактирование подписки на курс"""
    serializer_class = SubscriptionSerializer
    queryset = Subscribe.objects.all()
    permission_classes = (IsAuthenticated, Author | Moderator,)


class SubscribeDeleteAPIView(generics.DestroyAPIView):
    """Удаление подписки на курс"""
    serializer_class = SubscriptionSerializer
    queryset = Subscribe.objects.all()
    permission_classes = (IsAuthenticated,)
