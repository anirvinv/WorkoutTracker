from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Exercise(models.Model):
    user = models.ForeignKey(
        User, related_name='exercises', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    volume = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    rpe = models.FloatField()
    exercise_type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Stats(models.Model):
    user = models.ForeignKey(User, related_name='stats',
                             on_delete=models.CASCADE)
    weight = models.IntegerField()
    height = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weight} lb {self.height} in."
