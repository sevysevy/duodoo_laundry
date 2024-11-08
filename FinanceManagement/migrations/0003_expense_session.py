# Generated by Django 5.1.2 on 2024-11-08 05:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
        ('FinanceManagement', '0002_expense_partner_alter_expense_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.salesession'),
        ),
    ]