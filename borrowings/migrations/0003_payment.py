# Generated by Django 5.0.4 on 2024-04-26 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowings', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], max_length=7)),
                ('type', models.CharField(choices=[('PAYMENT', 'Payment'), ('FINE', 'Fine')], max_length=7)),
                ('session_url', models.URLField()),
                ('session_id', models.CharField(max_length=255)),
                ('money_to_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('borrowing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='borrowings.borrowing')),
            ],
        ),
    ]