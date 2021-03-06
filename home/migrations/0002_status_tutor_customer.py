# Generated by Django 4.0 on 2021-12-19 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, null=True)),
                ('image', models.ImageField(null=True, upload_to='tutor/')),
                ('cert', models.FileField(default='tutor/certificate.png', null=True, upload_to='tutor/')),
                ('address', models.CharField(max_length=100, null=True)),
                ('qualification', models.CharField(max_length=100, null=True)),
                ('experience', models.IntegerField(default=0)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.status')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subject')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='customer/')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
