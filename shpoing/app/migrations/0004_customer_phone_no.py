# Generated by Django 3.2.7 on 2021-09-04 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_user_product_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_no',
            field=models.IntegerField(max_length=9, null=True),
        ),
    ]
