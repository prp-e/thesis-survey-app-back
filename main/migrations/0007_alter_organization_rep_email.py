# Generated by Django 3.2.4 on 2021-07-09 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210626_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='rep_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]