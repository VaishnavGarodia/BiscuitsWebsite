# Generated by Django 3.1.1 on 2020-11-02 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biscuitsrk', '0015_auto_20201102_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='discord',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
