# Generated by Django 3.1.3 on 2020-11-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20201112_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseinstance',
            name='started',
            field=models.DateField(auto_now=True),
        ),
    ]
