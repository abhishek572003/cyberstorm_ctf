# Generated by Django 5.1.7 on 2025-03-14 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_team_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_professional',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='member_phones',
            field=models.TextField(blank=True),
        ),
    ]
