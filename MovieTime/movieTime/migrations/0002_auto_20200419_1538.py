# Generated by Django 2.2 on 2020-04-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieTime', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shows',
            name='theater_name',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.FileField(upload_to=''),
        ),
    ]
