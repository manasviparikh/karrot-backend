# Generated by Django 3.2.10 on 2021-12-31 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_generate_usernames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
