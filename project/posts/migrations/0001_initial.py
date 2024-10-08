# Generated by Django 3.1.4 on 2024-06-12 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iternary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2000)),
                ('no_of_days', models.IntegerField()),
                ('expenditure', models.IntegerField()),
                ('registration_timestamp', models.DateField(auto_now_add=True, null=True)),
                ('travellor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('media', models.ImageField(upload_to='iternary_images')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('iternary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.iternary')),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=2000)),
                ('starting_day', models.IntegerField()),
                ('iternary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.iternary')),
            ],
            options={
                'verbose_name': 'Destination',
                'verbose_name_plural': 'Destinations',
                'ordering': ['starting_day'],
            },
        ),
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=200)),
                ('location', models.URLField()),
                ('price', models.IntegerField()),
                ('review', models.TextField(max_length=2000)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.destination')),
            ],
            options={
                'verbose_name': 'Accomodation',
                'verbose_name_plural': 'Accomodations',
                'ordering': ['destination__starting_day'],
            },
        ),
    ]
