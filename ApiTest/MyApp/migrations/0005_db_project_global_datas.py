# Generated by Django 2.2 on 2022-05-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0004_db_project_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='global_datas',
            field=models.CharField(max_length=100, null=True),
        ),
    ]