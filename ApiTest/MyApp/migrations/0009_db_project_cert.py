# Generated by Django 2.2 on 2022-05-06 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0008_auto_20220506_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='cert',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
