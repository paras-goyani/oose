# Generated by Django 3.1.7 on 2021-03-17 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ottapp', '0003_auto_20210317_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='plan',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='user_plan',
            name='plan_name',
            field=models.CharField(default='', max_length=10),
        ),
    ]