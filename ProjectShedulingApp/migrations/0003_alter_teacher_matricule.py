# Generated by Django 5.2 on 2025-05-04 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectShedulingApp', '0002_alter_teacher_matricule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='matricule',
            field=models.CharField(default='00000', max_length=50, unique=True),
        ),
    ]
