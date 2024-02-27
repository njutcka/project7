from calendar import monthrange

from celery import shared_task
from education.models import Course
from datetime import datetime, timedelta, timezone
from education.services import mailing_util
from users.models import User


@shared_task
def send_updates(inst):
    course = Course.objects.get(pk=inst)
    # now = datetime.now()
    # no_spam_time = now - timedelta(hours=4)
    # if course.updated_at.timestamp() > no_spam_time.timestamp():
    #     return
    # else:
    subscribers = course.subscribe.all()
    subscribers_list = [subscribe.user for subscribe in subscribers]
    mailing_util(
        subject='Course were updated!',
        message=f'You get update in {course}!',
        recipient_list=subscribers_list,
    )
    print('Sent')


@shared_task
def inactive_user():
    now = datetime.now(tz=timezone.utc)
    month = now.month
    year = now.year
    days_count = monthrange(year, month)
    time_for_deactivate = now - timedelta(days=days_count[1])
    user_list = User.objects.filter(last_login__lte=time_for_deactivate, is_active=True)
    user_list.update(is_active=False)