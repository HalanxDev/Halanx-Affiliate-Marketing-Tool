# Generated by Django 2.2.1 on 2019-05-19 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0006_houseownerreferral_house_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='houseownerreferral',
            name='converted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tenantreferral',
            name='converted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]