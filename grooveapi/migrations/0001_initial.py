# Generated by Django 4.1 on 2022-09-05 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=50)),
                ('artist_description', models.CharField(max_length=250)),
                ('artist_image', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='GrooveUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=55)),
                ('profile_image', models.ImageField(null=True, upload_to='profileimages')),
                ('bio', models.CharField(max_length=250)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_name', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='grooveapi.artist')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='grooveapi.stage')),
            ],
        ),
        migrations.CreateModel(
            name='MyLineup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groove_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineupshows', to='grooveapi.grooveuser')),
            ],
        ),
        migrations.CreateModel(
            name='LineupShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_lineup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_shows', to='grooveapi.mylineup')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineup_shows', to='grooveapi.show')),
            ],
        ),
    ]