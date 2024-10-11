# Generated by Django 5.1 on 2024-10-10 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_userprofile_availability_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='events',
            new_name='joined_events',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='applied_events',
            field=models.ManyToManyField(blank=True, related_name='applicants', to='api.event'),
        ),
    ]
