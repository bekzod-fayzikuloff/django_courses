# Generated by Django 3.0 on 2021-12-24 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_auto_20211224_2149"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="category",
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]