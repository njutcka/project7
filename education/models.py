from django.db import models

from users.models import NULLABLE


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

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
