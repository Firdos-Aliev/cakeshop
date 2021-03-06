import string
import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from cakeshop.settings import USER_EXPIRES_TIMEDELTA, USER_SIZE_KEY, DOMAIN_NAME, EMAIL_HOST_USER


def get_activation_key():
    key = ''
    for i in range(USER_SIZE_KEY):
        key += random.choice(string.ascii_letters)
    return key


def get_activation_key_expires():
    return now() + USER_EXPIRES_TIMEDELTA


class CakeShopUser(AbstractUser):
    age = models.IntegerField(verbose_name='Возраст', null=True, blank=True)
    img = models.ImageField(verbose_name='Картинка', upload_to="user_img", blank=True)
    activation_key = models.CharField(max_length=USER_SIZE_KEY, blank=True, default=get_activation_key)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expires)

    # is_active = models.BooleanField(default=False) #не понимаю почему вставялет время

    # def save_user_profile(self):
    #    if CakeShopUserProfile.objects.filter(user=self).first() == None:
    #        CakeShopUserProfile.objects.create(user=self)
    #    else:
    #        self.cakeshopuserprofile.save()

    def verification_email(self):
        link = reverse("auth:user_verify",
                       kwargs={
                           "pk": self.pk,
                           "key": self.activation_key,
                       }
                       )
        title = "Verify Mail"
        message = f"Go to link to confirm: {DOMAIN_NAME}{link}"

        return self.email_user(title, message, EMAIL_HOST_USER)

    def valid_activation_key(self):
        return now() + USER_EXPIRES_TIMEDELTA > self.activation_key_expires

    @cached_property
    def basket_items(self):
        return self.basket_set.all()

    def total_sum(self):
        sum = 0
        for i in self.basket_items:
            sum += i.product.price * i.count
        return sum

    def total_count(self):
        count = 0
        for i in self.basket_items:
            count += i.count
        return count


class CakeShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(CakeShopUser, primary_key=True,
                                on_delete=models.CASCADE)

    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDER_CHOICES, blank=True)
    text = models.TextField(verbose_name='о себе', max_length=512,
                            blank=True)


@receiver(post_save, sender=CakeShopUser)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        CakeShopUserProfile.objects.create(user=instance)
