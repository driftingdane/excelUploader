# Generated by Django 4.2.1 on 2023-05-28 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verb', '0006_alter_verbaudio_verb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verbaudio',
            name='verb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_files', to='verb.verb'),
        ),
    ]