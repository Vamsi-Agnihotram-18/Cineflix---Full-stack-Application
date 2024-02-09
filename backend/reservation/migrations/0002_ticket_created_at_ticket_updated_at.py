# Generated by Django 4.2.6 on 2023-11-27 23:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
