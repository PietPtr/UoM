# Generated by Django 3.1.3 on 2020-11-09 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0007_auto_20201109_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_actions', models.ManyToManyField(to='teacher.Action')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_courses', models.ManyToManyField(to='student.CourseInstance')),
            ],
        ),
    ]
