# Generated by Django 5.1.2 on 2024-10-22 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_personaje_edad'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaje',
            name='imagen_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personaje',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
