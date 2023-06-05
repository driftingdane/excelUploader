from django.db import models


class VerbCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Verb(models.Model):
    infinitive = models.CharField(max_length=100)
    english_translation = models.CharField(max_length=100)
    danish_translation = models.CharField(max_length=100)
    category = models.ForeignKey(VerbCategory, on_delete=models.CASCADE)
    eu = models.CharField(max_length=100)
    voce_ele_ela = models.CharField(max_length=100)
    nos = models.CharField(max_length=100)
    voces_eles_elas = models.CharField(max_length=100)

    def __str__(self):
        return self.infinitive


class VerbAudio(models.Model):
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE, related_name='audio_files')
    audio = models.FileField(upload_to='audio')

    def __str__(self):
        return self.verb.infinitive
