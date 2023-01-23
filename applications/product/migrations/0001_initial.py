# Generated by Django 4.1.5 on 2023-01-21 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Категория')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание')),
                ('produced_date', models.DateField(verbose_name='Дата производства')),
                ('expired_date', models.DateField(verbose_name='Дата истечения срока использование')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('producer', models.CharField(max_length=250, verbose_name='Производитель')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.PositiveIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='product.category')),
                ('name', models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL, verbose_name='Название')),
            ],
        ),
    ]