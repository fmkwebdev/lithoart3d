# Generated by Django 3.0.3 on 2023-07-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_delete_mymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderconfirmation',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
