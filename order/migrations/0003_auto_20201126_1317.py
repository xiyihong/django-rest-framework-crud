# Generated by Django 2.2.13 on 2020-11-26 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_pay_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='pay_time',
        ),
        migrations.AddField(
            model_name='order',
            name='order_pay_at',
            field=models.DateTimeField(auto_now=True, verbose_name='订单付款时间'),
        ),
    ]
