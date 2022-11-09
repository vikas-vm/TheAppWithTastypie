# Generated by Django 4.0 on 2022-11-07 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='item',
            name='store',
            field=models.ManyToManyField(to='merchant.Store'),
        ),
    ]
