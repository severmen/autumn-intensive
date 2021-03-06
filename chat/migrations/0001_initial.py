# Generated by Django 3.2.7 on 2021-09-13 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nikname', models.CharField(max_length=150)),
                ('data_time', models.DateTimeField(default=datetime.datetime.now)),
                ('message', models.CharField(max_length=400)),
            ],
            options={
                'ordering': ['-data_time'],
            },
        ),
    ]
