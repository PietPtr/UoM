# Generated by Django 3.1.3 on 2020-11-07 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='action',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.action'),
        ),
    ]