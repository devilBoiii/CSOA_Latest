# Generated by Django 5.0.6 on 2024-07-24 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cso_app', '0039_cso_rankings'),
    ]

    operations = [
        migrations.AddField(
            model_name='cso_rankings',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
