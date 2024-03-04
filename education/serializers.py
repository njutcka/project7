from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField, IntegerField

from education.models import Course, Lesson, Payment, Subscribe
from education.validators import validate_data


class LessonSerializer(ModelSerializer):
    title = CharField(validators=(validate_data,))
    description = CharField(validators=(validate_data,))
    video = CharField(validators=(validate_data,))

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    title = CharField(validators=(validate_data,))
    description = CharField(validators=(validate_data,))
    count_lessons = IntegerField(source='lesson_set.all.count', read_only=True)  # поле количества уроков курса
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)  # поле вывода уроков
    is_subscribe = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribe(self, course):
        user = self.context['request'].user
        subscription = Subscribe.objects.filter(course=course.pk, user=user.pk, is_subscribe=True)
        if subscription:
            return True
        return False


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('is_subscribe',)