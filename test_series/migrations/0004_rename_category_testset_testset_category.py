# Generated by Django 4.0.4 on 2022-06-26 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_series', '0003_testsetcategory_testset_testseries_testset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testset',
            old_name='category',
            new_name='testset_category',
        ),
    ]