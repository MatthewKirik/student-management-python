# Generated by Django 4.2.1 on 2023-06-04 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]
