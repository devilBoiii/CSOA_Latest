# Generated by Django 5.0.6 on 2024-08-21 11:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cso_app', '0084_notifications_author_notifications_remarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notifications_id',
            field=models.UUIDField(default=uuid.UUID('1a46b93d-05f3-4166-acbb-fc86f85747d6'), editable=False, primary_key=True, serialize=False),
        ),
    ]
