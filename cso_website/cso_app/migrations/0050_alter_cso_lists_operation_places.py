# Generated by Django 5.0.6 on 2024-07-30 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cso_app', '0049_alter_cso_lists_po_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cso_lists',
            name='operation_places',
            field=models.TextField(blank=True, null=True),
        ),
    ]
