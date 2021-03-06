# Generated by Django 3.0 on 2021-12-24 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_auto_20211224_2207"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="course",
        ),
        migrations.RemoveField(
            model_name="teacher",
            name="course",
        ),
        migrations.AddField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(blank=True, null=True, to="courses.Student"),
        ),
        migrations.AddField(
            model_name="course",
            name="teachers",
            field=models.ManyToManyField(blank=True, null=True, to="courses.Teacher"),
        ),
    ]
