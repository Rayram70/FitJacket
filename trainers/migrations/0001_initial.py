# Generated by Django 5.2 on 2025-04-18 02:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('specialties', models.CharField(help_text='e.g., Strength, Cardio, Yoga', max_length=255)),
                ('rate_per_session', models.DecimalField(decimal_places=2, max_digits=6)),
                ('available_times', models.TextField(help_text='Describe your weekly availability')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
