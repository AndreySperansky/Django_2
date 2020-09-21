from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver



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
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    # age = models.PositiveIntegerField(verbose_name='возраст')
    sex = models.CharField(max_length=6, choices=SEX_CHOICE, default=SEX_OTHER, verbose_name='Пол')  # male, female

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

    # ***********************************************************************************************************
    # One-To-One
    # ***********************************************************************************************************


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128,  blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)


    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()

    
    