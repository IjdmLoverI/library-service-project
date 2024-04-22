# Generated by Django 5.0.4 on 2024-04-22 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('cover', models.CharField(choices=[('HARD', 'Hard cover'), ('SOFT', 'Soft cover')], max_length=4)),
                ('inventory', models.PositiveIntegerField(default=0)),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
