# Generated by Django 2.2 on 2020-04-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieTime', '0003_auto_20200419_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='logo',
        ),
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='posters'),
        ),
    ]
