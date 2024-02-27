import smtplib
import stripe
from django.conf import settings
from django.core.mail import send_mail


class StripePayments:
    def __init__(self, user, amount, course=None, lesson=None):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_API_KEY
        self.course = course
        self.lesson = lesson
        self.user = user
        self.amount = amount

    def create_session(self):
        if self.course:
            product = self.course
        elif self.lesson:
            product = self.lesson
        else:
            product = 'Undefined'
        price = stripe.Price.create(
            currency="rub",
            unit_amount=int(self.amount),
            # recurring={"interval": "month"},
            product_data={"name": product},
        )
        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": price.get('id'), "quantity": 1}],
            mode="payment",
        )
        data = {
            'session_id': session.get('id', None),
            'url_pay': session.get('url', None)
        }
        return data

    @staticmethod
    def retrieve_session(session_id):

        stripe.api_key = settings.STRIPE_API_KEY
        get_session = stripe.checkout.Session.retrieve(session_id)
        return get_session.get('payment_status')


def mailing_util(subject: str,
                 message: str,
                 recipient_list: list,
                 from_email=settings.EMAIL_HOST_USER
                 ):
    try:
        status_send = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list
        )
    except smtplib.SMTPException:
        raise smtplib.SMTPException
