# Generated by Django 4.0.9 on 2024-05-23 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_goelectricrebateapplication_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeRedeemedGoElectricRebateApplication',
            fields=[
            ],
            options={
                'ordering': ['-modified'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('api.goelectricrebateapplication',),
        ),
    ]
