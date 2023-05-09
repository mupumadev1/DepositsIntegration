# Generated by Django 4.1.7 on 2023-05-03 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [

        migrations.AddField(
            model_name='processeddeposits',
            name='transaction_date',
            field=models.CharField(default='2023-04-26', max_length=255, unique=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processeddeposits',
            name='vendorname',
            field=models.CharField(default='Funwell Malake', max_length=255),
            preserve_default=False,
        ),
    ]
