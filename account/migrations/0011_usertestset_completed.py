# Generated by Django 4.0.4 on 2022-06-30 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_usertestset_usertestsetanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestset',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
