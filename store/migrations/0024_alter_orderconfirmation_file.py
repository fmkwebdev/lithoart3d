# Generated by Django 4.2.4 on 2024-01-02 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_alter_orderconfirmation_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderconfirmation',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
