# Generated by Django 5.1.7 on 2025-03-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_team_created_at_teammember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
