# Generated by Django 4.2.1 on 2023-05-27 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verb', '0004_alter_verbaudio_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verbaudio',
            name='verb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_files', to='verb.verb'),
        ),
    ]