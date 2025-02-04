# Generated by Django 5.0.1 on 2024-07-10 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0009_emailinpv31_lectorpin_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateField()),
                ('hash', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pincode',
            name='lector_pin',
        ),
        migrations.AddField(
            model_name='pincode',
            name='order',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='pincode',
            name='course_pin',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.course'),
        ),
    ]
