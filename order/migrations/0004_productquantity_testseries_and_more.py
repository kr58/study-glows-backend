# Generated by Django 4.0.4 on 2022-06-07 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_series', '0002_feature2_description_alter_testseries_category_and_more'),
        ('order', '0003_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='productquantity',
            name='testseries',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test_series.testseries'),
        ),
        migrations.AlterField(
            model_name='productquantity',
            name='type',
            field=models.CharField(blank=True, choices=[('course', 'course'), ('testseries', 'testseries')], max_length=216, null=True),
        ),
    ]