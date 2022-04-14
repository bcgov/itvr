# Generated by Django 4.0.1 on 2022-04-14 22:19

import api.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import encrypted_fields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoElectricRebateApplication',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sin', encrypted_fields.fields.EncryptedCharField(max_length=9, validators=[api.validators.validate_sin])),
                ('last_name', models.CharField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('middle_names', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('postal_code', models.CharField(max_length=6)),
                ('drivers_licence', models.CharField(max_length=8, validators=[django.core.validators.MinLengthValidator(7)])),
                ('date_of_birth', models.DateField(validators=[api.validators.validate_driving_age])),
                ('tax_year', models.IntegerField()),
                ('doc1', models.ImageField(upload_to='docs')),
                ('doc2', models.ImageField(upload_to='docs')),
                ('verified', models.BooleanField()),
                ('spouse_email', models.EmailField(blank=True, max_length=250, null=True)),
                ('application_type', models.CharField(max_length=25)),
                ('consent_personal', models.BooleanField(validators=[api.validators.validate_consent])),
                ('consent_tax', models.BooleanField(validators=[api.validators.validate_consent])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'go_electric_rebate_application',
            },
        ),
        migrations.CreateModel(
            name='HouseholdMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('sin', encrypted_fields.fields.EncryptedCharField(max_length=9)),
                ('last_name', models.CharField(max_length=250)),
                ('first_name', models.CharField(max_length=250)),
                ('middle_names', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(max_length=250)),
                ('date_of_birth', models.DateField()),
                ('doc1', models.ImageField(upload_to='docs')),
                ('doc2', models.ImageField(upload_to='docs')),
                ('verified', models.BooleanField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.goelectricrebateapplication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'household_member',
            },
        ),
    ]
