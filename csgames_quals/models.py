from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    participants = models.ManyToManyField('Participant', null=True, blank=True, related_name='competitions')


class Participant(models.Model):
    name = models.CharField(max_length=75)
    preferences = models.ManyToManyField('Competition')