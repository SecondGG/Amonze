# Generated by Django 3.2.5 on 2022-03-26 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_amonze', '0002_auto_20220325_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
