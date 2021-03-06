# Generated by Django 3.1.5 on 2021-04-27 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_listing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imgURL',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
