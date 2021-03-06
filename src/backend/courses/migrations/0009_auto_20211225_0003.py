# Generated by Django 3.0 on 2021-12-25 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0008_auto_20211225_0001"),
    ]

    operations = [
        migrations.AddField(
            model_name="homework",
            name="file",
            field=models.FileField(default="", upload_to="media/homeworks/%Y/%m/%d"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="course",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="owner", to="courses.Teacher"
            ),
        ),
    ]
