# Generated by Django 4.1.5 on 2023-01-24 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=True, max_length=250, unique=True),
        ),
    ]
