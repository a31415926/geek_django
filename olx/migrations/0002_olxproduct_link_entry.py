# Generated by Django 3.1.5 on 2021-02-21 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='olxproduct',
            name='link_entry',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]