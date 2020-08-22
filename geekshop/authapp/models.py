from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta




class ShopUser(AbstractUser):
    
    SEX_MAIL = 'mail'
    SEX_FEMAIL = 'femail'
    SEX_OTHER = 'other'
    
    SEX_CHOICE = (
        (SEX_MAIL, 'Мужской'),
        (SEX_FEMAIL, 'Женский'),
        (SEX_OTHER, 'Не указан')
    )
    
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст')
    sex = models.CharField(max_length = 6, choices=SEX_CHOICE, default = SEX_OTHER, verbose_name = 'Пол') # male, female
    
    # ***********************************************************************************************************
    # Django2
    # ***********************************************************************************************************
    
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))


    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    