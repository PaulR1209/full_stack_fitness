# Generated by Django 5.1.1 on 2024-11-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0015_remove_order_change_count_order_has_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
