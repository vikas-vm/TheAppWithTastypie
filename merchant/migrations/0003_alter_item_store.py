# Generated by Django 4.0 on 2022-11-09 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0002_remove_merchant_is_active_alter_item_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='store',
            field=models.ManyToManyField(blank=True, related_name='items', to='merchant.Store'),
        ),
    ]
