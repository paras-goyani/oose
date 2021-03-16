from django.db import models

# Create your models here.

class Movie(models.Model):
    #course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200, null=False)
    content = models.CharField(max_length=100000, null=False)
    video_720p = models.CharField(max_length=200, null=False)
    video_480p = models.CharField(max_length=200, null=False)
    video_360p = models.CharField(max_length=200, null=False)
    video_240p = models.CharField(max_length=200, null=False)
    video_144p = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.title