import time
from django.core.mail import send_mail
from main.celery import app


@app.task
def send_confirmation_email_celery(email, code):
    time.sleep(5)
    full_link = f'http://localhost:8000/accounts/activate/{code}'
    send_mail(
        'Активация пользователя',
        full_link,
        'kadirbekova43@gmail.com',
        [email]
    )
@app.task
def send_confirmation_code_celery(email, code):
    time.sleep(1)
    send_mail(
        'Восстановление пароля',
        code,
        'Kadirbekova43@gmail.com',
        [email]
    )
