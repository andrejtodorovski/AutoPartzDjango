# Generated by Django 4.1.7 on 2023-06-12 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autopartz', '0002_customuser_email_alter_customuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autopartz.customuser'),
        ),
    ]
