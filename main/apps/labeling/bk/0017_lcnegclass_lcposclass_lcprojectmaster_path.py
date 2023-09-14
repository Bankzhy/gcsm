# Generated by Django 4.0.6 on 2022-11-11 13:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('labeling', '0016_lcprojectmaster'),
    ]

    operations = [
        migrations.CreateModel(
            name='LCNegClass',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=100)),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('path', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'lc_neg_class',
            },
        ),
        migrations.CreateModel(
            name='LCPosClass',
            fields=[
                ('class_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=100)),
                ('extra_method', models.CharField(max_length=255)),
                ('extra_field', models.CharField(max_length=255)),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('path', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'lc_pos_class',
            },
        ),
        migrations.AddField(
            model_name='lcprojectmaster',
            name='path',
            field=models.CharField(default='', max_length=255),
        ),
    ]
