# Generated by Django 4.1.7 on 2023-06-14 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopartz', '0005_car_part_compatible_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='engine_displacement',
            field=models.IntegerField(),
        ),
    ]
