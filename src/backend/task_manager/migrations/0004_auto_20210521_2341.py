# Generated by Django 3.0.4 on 2021-05-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_auto_20210521_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='avatar',
            field=models.FileField(blank=True, max_length=80, null=True, upload_to='avatar/%Y/%m/%d'),
        ),
    ]