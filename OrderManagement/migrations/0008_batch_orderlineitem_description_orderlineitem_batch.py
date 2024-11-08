# Generated by Django 5.1.2 on 2024-10-31 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0007_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_id', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Laundry', 'In Laundry'), ('Returned', 'Returned'), ('Completed', 'Completed')], max_length=20)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='orderlineitem',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='orderlineitem',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='OrderManagement.batch'),
        ),
    ]
