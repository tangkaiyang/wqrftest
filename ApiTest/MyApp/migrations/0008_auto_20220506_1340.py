# Generated by Django 2.2 on 2022-05-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0007_auto_20220506_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_step',
            name='sign',
            field=models.CharField(default='no', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='db_apis',
            name='sign',
            field=models.CharField(default='no', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='db_login',
            name='sign',
            field=models.CharField(default='no', max_length=10, null=True),
        ),
    ]
