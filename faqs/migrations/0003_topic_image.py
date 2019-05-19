# Generated by Django 2.2.1 on 2019-05-18 16:15

from django.db import migrations, models
import faqs.utils


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0002_auto_20190518_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=faqs.utils.get_topic_image_upload_path),
        ),
    ]