# Generated by Django 5.0.6 on 2024-06-20 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_sys', '0003_rename_titel_portfolioprojects_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
