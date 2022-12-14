# Generated by Django 4.1.1 on 2022-10-20 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=40)),
                ('author', models.CharField(default='', max_length=30)),
                ('amount', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'books',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='', max_length=255)),
                ('password', models.CharField(default='', max_length=128)),
                ('email', models.CharField(default='', max_length=255)),
                ('handle', models.CharField(default='', max_length=255)),
                ('role', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
