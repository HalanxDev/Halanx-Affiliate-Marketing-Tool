# Generated by Django 2.2.1 on 2019-05-20 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0012_auto_20190519_2258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='qrcoderequest',
            options={'ordering': ('-timestamp',)},
        ),
    ]
