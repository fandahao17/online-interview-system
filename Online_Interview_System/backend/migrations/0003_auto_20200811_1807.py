# Generated by Django 3.1 on 2020-08-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20200811_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hr',
            options={'verbose_name': 'HR', 'verbose_name_plural': 'HR'},
        ),
        migrations.AlterModelOptions(
            name='interviewee',
            options={'verbose_name': '候选人', 'verbose_name_plural': '候选人'},
        ),
        migrations.AlterModelOptions(
            name='interviewer',
            options={'verbose_name': '面试官', 'verbose_name_plural': '面试官'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': '面试房间', 'verbose_name_plural': '面试房间'},
        ),
        migrations.AlterModelOptions(
            name='super',
            options={'verbose_name': '超级管理员', 'verbose_name_plural': '超级管理员'},
        ),
        migrations.AlterField(
            model_name='room',
            name='finaleval',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='tempeval',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
