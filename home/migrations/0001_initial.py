# Generated by Django 4.0 on 2021-12-17 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('sub_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_name', models.CharField(max_length=50)),
                ('sub_desc', models.TextField()),
            ],
        ),
    ]
