# Generated by Django 5.0.1 on 2024-07-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0008_emailinpv31_pincode_name_surname'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectorpin',
            name='hash',
            field=models.CharField(blank=True, default=None, max_length=150, null=True, unique=True),
        ),
    ]
