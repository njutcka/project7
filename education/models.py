from django.db import models

from config import settings
from users.models import NULLABLE, User


class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='название курса')
    course_preview = models.ImageField(upload_to='education/', verbose_name='превью курса', **NULLABLE)
    course_description = models.CharField(max_length=500, verbose_name='описание курса', **NULLABLE)

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name='название урока')
    lesson_preview = models.ImageField(upload_to='education/', verbose_name='превью урока', **NULLABLE)
    lesson_description = models.CharField(max_length=500, verbose_name='описание урока', **NULLABLE)
    lesson_url = models.CharField(max_length=500, verbose_name='ссылка на урок', **NULLABLE)
    course = models.ForeignKey(Course, **NULLABLE, on_delete=models.CASCADE, verbose_name='Урок курса')


    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    CARD = "Безналичный"
    CASH = "Наличные"

    PAYMENT_METHOD = [
        (CARD, "Безналичный"),
        (CASH, "Наличные"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(**NULLABLE, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Оплаченный урок')
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_METHOD, default=CARD, max_length=100, **NULLABLE,
                                      verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user}: {self.paid_course} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription', verbose_name='курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    is_subscription = models.BooleanField(default=True, verbose_name='признак подписки')

    def __str__(self):
        return f'{self.user} - {self.course}: {self.is_subscription}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
