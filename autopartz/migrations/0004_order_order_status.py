# Generated by Django 4.1.7 on 2023-06-12 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopartz', '0003_alter_shoppingcart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('In progress', 'In progress'), ('Delivered', 'Delivered')], default='In progress', max_length=100),
            preserve_default=False,
        ),
    ]
