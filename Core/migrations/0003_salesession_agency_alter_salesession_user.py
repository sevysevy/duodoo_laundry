# Generated by Django 5.1.2 on 2024-11-11 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_salesession_added_fund_salesession_closing_fund_and_more'),
        ('UserManagement', '0003_agency'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesession',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagement.agency'),
        ),
        migrations.AlterField(
            model_name='salesession',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagement.userprofile'),
        ),
    ]
