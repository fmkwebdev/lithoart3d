# Generated by Django 4.2.4 on 2023-12-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_delete_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='leiras_sr',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='namesr',
            field=models.CharField(default=False, max_length=100),
        ),
    ]
