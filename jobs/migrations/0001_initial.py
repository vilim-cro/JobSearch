# Generated by Django 3.1.1 on 2021-04-24 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobtitle', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=69420)),
                ('about', models.CharField(max_length=69420)),
            ],
        ),
    ]