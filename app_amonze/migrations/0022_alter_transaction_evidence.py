# Generated by Django 3.2.5 on 2022-04-29 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_amonze', '0021_alter_transaction_evidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='evidence',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
