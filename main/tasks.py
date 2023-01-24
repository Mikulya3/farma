from django.contrib.auth import get_user_model

from applications.spam.models import Spam
from main.celery import app
from django.core.mail import send_mail


User = get_user_model()
@app.task
def spam_message():
    emails = User.objects.all()
    list_email = [i.email for i in emails]
    for email in emails:
        send_mail(
            'вас привествует аптека, надеемся вы живы!',
            'У нас акция на памперсы! 10 штук по супер цене 250 сом за упаковку! ждем вас по адресу Токтогула 175',
            'kadirbekova43@gmail.com',
            list_email
        )