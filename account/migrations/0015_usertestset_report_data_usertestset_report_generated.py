# Generated by Django 4.0.4 on 2022-07-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_rename_option_usertestsetanswer_selected_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestset',
            name='report_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usertestset',
            name='report_generated',
            field=models.CharField(blank=True, choices=[('generated', 'generated'), ('incomplete', 'incomplete'), ('not_generated', 'not_generated')], max_length=512, null=True),
        ),
    ]
