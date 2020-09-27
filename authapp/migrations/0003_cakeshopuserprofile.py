# Generated by Django 2.2 on 2020-09-26 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20200923_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='CakeShopUserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(blank=True, choices=[('M', 'мужской'), ('W', 'женский')], max_length=1, verbose_name='пол')),
                ('text', models.TextField(blank=True, max_length=512, verbose_name='о себе')),
            ],
        ),
    ]
