# Generated by Django 4.0.4 on 2022-07-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_series', '0010_testsetquestion_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(blank=True, choices=[('mcq', 'mcq'), ('cq', 'cq')], max_length=512, null=True),
        ),
    ]