# Generated by Django 2.2 on 2022-04-24 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0006_db_apis_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]