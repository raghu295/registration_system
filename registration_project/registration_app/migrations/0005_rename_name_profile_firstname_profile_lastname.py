# Generated by Django 4.2.7 on 2023-12-28 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0004_contact_remove_profile_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='profile',
            name='lastname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
