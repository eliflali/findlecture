# Generated by Django 4.2.7 on 2024-02-10 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('course_name', models.CharField(max_length=255)),
                ('course_code', models.CharField(max_length=20)),
                ('course_link', models.URLField()),
                ('course_contents', models.TextField()),
            ],
        ),
    ]
