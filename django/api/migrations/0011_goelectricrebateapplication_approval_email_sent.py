# Generated by Django 4.0.1 on 2022-08-25 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_cancellablegoelectricrebateapplication_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='goelectricrebateapplication',
            name='approval_email_sent',
            field=models.BooleanField(null=True),
        ),
    ]
