# Generated by Django 2.2.3 on 2019-07-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='num_results',
            field=models.BigIntegerField(),
        ),
    ]
