# Generated by Django 5.1 on 2024-10-02 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_app', '0020_rename_view_count_product_add_to_cart_count_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_no', models.CharField(blank=True, max_length=10, null=True)),
                ('street', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=2)),
                ('state', models.CharField(max_length=100)),
                ('state_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('city_code', models.CharField(max_length=10)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='delivery_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic_app.location'),
        ),
    ]