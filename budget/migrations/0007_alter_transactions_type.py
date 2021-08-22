# Generated by Django 3.2.6 on 2021-08-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_alter_transactions_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='type',
            field=models.CharField(blank=True, choices=[('INCOME', 'INCOME'), ('EXPENSE', 'EXPENSE')], max_length=200, null=True),
        ),
    ]