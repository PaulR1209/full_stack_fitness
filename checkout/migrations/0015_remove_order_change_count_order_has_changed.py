# Generated by Django 5.1.1 on 2024-11-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0014_order_change_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='change_count',
        ),
        migrations.AddField(
            model_name='order',
            name='has_changed',
            field=models.BooleanField(default=False),
        ),
    ]