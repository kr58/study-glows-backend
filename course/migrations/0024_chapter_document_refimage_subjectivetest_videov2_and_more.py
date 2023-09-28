# Generated by Django 4.2.5 on 2023-09-28 05:02

import datetime
from django.db import migrations, models
import django_enum.fields


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0020_delete_admin"),
        ("course", "0023_coursesectionlecture_is_demo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=2048)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(blank=True, max_length=2048, null=True)),
                ("url", models.CharField(max_length=2048)),
                ("size", models.PositiveBigIntegerField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="RefImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(blank=True, max_length=2048, null=True)),
                ("url", models.CharField(max_length=2048)),
                ("size", models.PositiveBigIntegerField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="SubjectiveTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(blank=True, max_length=2048, null=True)),
                ("url", models.CharField(max_length=2048)),
                ("size", models.PositiveBigIntegerField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="VideoV2",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(blank=True, max_length=2048, null=True)),
                ("url", models.CharField(max_length=2048)),
                ("length", models.PositiveBigIntegerField()),
                ("size", models.PositiveBigIntegerField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="CourseV2",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("title", models.CharField(blank=True, max_length=1024, null=True)),
                ("thumbnail", models.TextField(blank=True, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                (
                    "language",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("English", "English"),
                            ("Hindi", "Hindi"),
                            ("Hinglish", "Hinglish"),
                        ],
                        max_length=512,
                        null=True,
                    ),
                ),
                ("price", models.FloatField(blank=True, default=0, null=True)),
                ("mrp", models.FloatField(blank=True, default=0, null=True)),
                (
                    "validity",
                    models.DateField(
                        blank=True, default=datetime.datetime.now, null=True
                    ),
                ),
                (
                    "publish",
                    models.DateField(
                        blank=True, default=datetime.datetime.now, null=True
                    ),
                ),
                (
                    "category",
                    django_enum.fields.EnumCharField(
                        blank=True,
                        choices=[
                            ("Academic", "ACADEMIC"),
                            ("Non-Academic", "NONACADEMIC"),
                        ],
                        max_length=12,
                    ),
                ),
                ("chapters", models.ManyToManyField(blank=True, to="course.chapter")),
                ("faq", models.ManyToManyField(blank=True, to="account.faq")),
                ("feature", models.ManyToManyField(blank=True, to="course.feature")),
                (
                    "instructor",
                    models.ManyToManyField(blank=True, to="course.instructor"),
                ),
            ],
            options={"ordering": ("-created_at",),},
        ),
        migrations.AddField(
            model_name="chapter",
            name="documents",
            field=models.ManyToManyField(blank=True, to="course.document"),
        ),
        migrations.AddField(
            model_name="chapter",
            name="images",
            field=models.ManyToManyField(blank=True, to="course.refimage"),
        ),
        migrations.AddField(
            model_name="chapter",
            name="tests",
            field=models.ManyToManyField(blank=True, to="course.subjectivetest"),
        ),
        migrations.AddField(
            model_name="chapter",
            name="videos",
            field=models.ManyToManyField(blank=True, to="course.videov2"),
        ),
    ]