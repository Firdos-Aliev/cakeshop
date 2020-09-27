from django.core.management.base import BaseCommand
from authapp.models import CakeShopUser, CakeShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in CakeShopUser.objects.filter(cakeshopuserprofile__isnull=True):
            CakeShopUserProfile.objects.create(user=i)

