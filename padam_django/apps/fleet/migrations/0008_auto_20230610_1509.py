# Generated by Django 3.2.5 on 2023-06-10 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0007_alter_busstop_shift'),
    ]

    operations = [
        migrations.RenameField(
            model_name='busshift',
            old_name='end_time',
            new_name='end_datetime',
        ),
        migrations.RenameField(
            model_name='busshift',
            old_name='start_time',
            new_name='start_datetime',
        ),
    ]
