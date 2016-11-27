# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-22 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NamesDatabase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('usuario', models.CharField(max_length=255)),
                ('accion', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
    ]