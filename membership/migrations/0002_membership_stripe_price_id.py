# Generated by Django 5.1.1 on 2024-10-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='stripe_price_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
