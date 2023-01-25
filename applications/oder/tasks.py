from main.celery import app
from django.core.mail import send_mail
@app.task
def send_confirmation_email(email, code, products, price):
    full_link = f'hi,confirm your order {products} {price} \n\n http://localhost:8000/api/v1/order/confirm/{code}'

    send_mail(
        f'Confirm your Orders',
        full_link,
        'kadirbekova43@gmail.com',
        [email]
    )