# Generated by Django 3.2.5 on 2022-04-07 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_amonze', '0013_auto_20220407_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='item',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='quantity',
        ),
        migrations.AddField(
            model_name='transaction',
            name='complete',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_amonze.item')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_amonze.transaction')),
            ],
        ),
    ]
