# Generated by Django 3.0.4 on 2020-05-02 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='cool', max_length=35),
            preserve_default=False,
        ),
    ]