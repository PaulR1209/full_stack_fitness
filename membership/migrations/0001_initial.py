# Generated by Django 5.1.1 on 2024-10-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold')], max_length=100)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]
