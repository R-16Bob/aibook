# Generated by Django 2.0 on 2021-06-23 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aibook_Model', '0005_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='uname',
            field=models.CharField(default='bob', max_length=30),
        ),
    ]
