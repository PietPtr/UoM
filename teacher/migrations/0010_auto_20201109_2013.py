# Generated by Django 3.1.3 on 2020-11-09 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0009_auto_20201109_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('course', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='teacher.course')),
            ],
        ),
    ]
