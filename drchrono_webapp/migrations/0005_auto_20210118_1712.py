# Generated by Django 3.1.5 on 2021-01-18 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono_webapp', '0004_auto_20210108_0256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorinformation',
            name='doctor_first_name',
        ),
        migrations.RemoveField(
            model_name='doctorinformation',
            name='doctor_id',
        ),
        migrations.RemoveField(
            model_name='doctorinformation',
            name='doctor_last_name',
        ),
    ]