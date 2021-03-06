# Generated by Django 2.2.1 on 2019-05-16 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0005_auto_20190515_2335'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateBankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(blank=True, max_length=200, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('account_type', models.CharField(blank=True, max_length=10, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=200, null=True)),
                ('bank_branch', models.CharField(blank=True, max_length=300, null=True)),
                ('bank_branch_address', models.CharField(blank=True, max_length=300, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=25, null=True)),
                ('affiliate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank_detail', to='affiliates.Affiliate')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
