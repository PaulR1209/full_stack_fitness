# Generated by Django 5.1.1 on 2024-10-11 15:02

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('membership', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_renewed', models.DateTimeField(auto_now=True)),
                ('next_renewal', models.DateTimeField()),
                ('is_paid', models.BooleanField(default=False)),
                ('cancellation_date', models.DateTimeField(blank=True, null=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.membership')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_history', to='checkout.order')),
            ],
        ),
        migrations.CreateModel(
            name='RecurringPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('next_payment_date', models.DateTimeField()),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurring_payments', to='checkout.order')),
            ],
        ),
    ]
