# Generated by Django 3.1.1 on 2020-11-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biscuitsrk', '0016_profile_discord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='checked',
            field=models.BooleanField(default=True),
        ),
    ]
