# Generated by Django 3.0.1 on 2020-02-26 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_option',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ProductOptions'),
        ),
    ]
