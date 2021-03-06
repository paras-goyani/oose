# Generated by Django 3.1.7 on 2021-03-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ottapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='subscription_plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('0', 'Basic'), ('1', 'Premium'), ('2', 'Cinematic')], max_length=20)),
                ('duration_day', models.IntegerField(default=0)),
                ('support', models.CharField(max_length=30)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
    ]
