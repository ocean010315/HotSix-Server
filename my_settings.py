# my_settings.py

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'workahallic',
        'USER' : 'root',
        'PASSWORD' : '0000',
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}

SECRET_KEY = 'django-insecure-a$p3j)^!uwllm2i+s4#)o9fk)h0z*sib7rk^mn&7!)$tadce%c'

EMAIL = {
    'EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS' : True,
    'EMAIL_PORT' : 587,
    'EMAIL_HOST' : 'smtp.gmail.com',
    'EMAIL_HOST_USER' : 'forproject5315@gmail.com',
    'EMAIL_HOST_PASSWORD' : 'jaokbspwktpnucjr',
    'SERVER_EMAIL' : 'forproject5315@gmail.com',
    'REDIRECT_PAGE' : '127.0.0.1:8000/user/register/' # 이동할 페이지로 수정해주기
}