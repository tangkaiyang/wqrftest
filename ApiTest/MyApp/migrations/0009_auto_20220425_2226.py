# Generated by Django 2.2 on 2022-04-25 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0008_db_steps'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DB_steps',
            new_name='DB_step',
        ),
    ]
