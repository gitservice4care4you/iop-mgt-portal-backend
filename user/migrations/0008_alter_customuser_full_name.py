# Generated by Django 5.1.2 on 2025-04-17 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_customuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(auto_created=True, default='<django.db.models.fields.CharField> <django.db.models.fields.CharField>', editable=False, max_length=255),
        ),
    ]
