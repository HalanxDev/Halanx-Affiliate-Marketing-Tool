# Generated by Django 2.2.1 on 2019-05-14 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True)),
                ('unique_code', models.TextField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AffiliateOccupationCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AffiliateOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=500, null=True)),
                ('affiliate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organisation', to='affiliates.Affiliate')),
            ],
        ),
        migrations.CreateModel(
            name='AffiliateOrganisationTypeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=30)),
                ('password', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AffiliateOrganisationAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('pincode', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('complete_address', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('organisation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='affiliates.AffiliateOrganisation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='affiliateorganisation',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organisations', to='affiliates.AffiliateOrganisationTypeCategory'),
        ),
        migrations.CreateModel(
            name='AffiliateAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('pincode', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('complete_address', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('affiliate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='affiliates.Affiliate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='affiliate',
            name='occupation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='affiliates', to='affiliates.AffiliateOccupationCategory'),
        ),
        migrations.AddField(
            model_name='affiliate',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='affiliate', to=settings.AUTH_USER_MODEL),
        ),
    ]
