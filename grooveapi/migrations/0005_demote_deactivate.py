# Generated by Django 4.1 on 2022-09-20 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grooveapi', '0004_alter_grooveuser_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approveUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='firstapproved', to='grooveapi.grooveuser')),
                ('demotedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demoted', to='grooveapi.grooveuser')),
                ('secondApproveUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondapproved', to='grooveapi.grooveuser')),
            ],
        ),
        migrations.CreateModel(
            name='Deactivate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approveUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='firstdeactiveapproved', to='grooveapi.grooveuser')),
                ('deactivatedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deactivate', to='grooveapi.grooveuser')),
                ('secondApproveUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seconddeactiveapproved', to='grooveapi.grooveuser')),
            ],
        ),
    ]