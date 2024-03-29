# Generated by Django 4.0.6 on 2022-08-08 09:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('labeling', '0006_alter_methodwaitmaster_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosMethodMaster',
            fields=[
                ('method_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('review_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('level', models.PositiveIntegerField(default=0)),
                ('ex_pos', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'long_method_master',
            },
        ),
        migrations.DeleteModel(
            name='LongMethodMaster',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='content',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='method_name',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='param_count',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='path',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='negmethodmaster',
            name='return_type',
        ),
        migrations.AddField(
            model_name='quesmaster',
            name='detail',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='negmethodmaster',
            name='method_id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
