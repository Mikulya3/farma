from django.core.mail import send_mail


def send_confirmation_email(email, code):
    full_link = f'http://34.107.6.37/api/v1/account/activate/{code}'
    send_mail(
        'User Activation',
        full_link,
        'Kadirbekova43@gmail.com',
        [email]
    )


def send_confirmation_code(email, code):
    send_mail(
        'Восстановление пароля',
        code,
        'Kadirbekova43@gmail.com',
        [email]
    )