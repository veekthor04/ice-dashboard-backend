# Generated by Django 3.2.12 on 2022-03-27 08:56

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_customer_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='0123456789ABCDEFGHJKLMNPQRSTUVWXYZ', db_index=True, editable=False, length=10, max_length=40, prefix='CUS_', unique=True),
        ),
    ]