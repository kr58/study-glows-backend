# Generated by Django 4.0.4 on 2022-06-11 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_resources_video_lecture_coursesection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='resourse',
            field=models.ManyToManyField(blank=True, to='course.resources'),
        ),
    ]
