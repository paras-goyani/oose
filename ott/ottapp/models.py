from django.db import models

# Create your models here.

class Movie(models.Model):
    movie_name = models.CharField(max_length=200 ,null=True ,blank=True,default='')
    poster = models.CharField(max_length=200,null=True ,blank=True,default='')
    genre = models.CharField(max_length=200,null=True ,blank=True,default='')
    release_date = models.DateField(blank=True,null=True,default='0000-00-00')
    ratting = models.FloatField(default=0)
    running_time = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, null=True,blank=True,default='')
    video = models.CharField(max_length=500, null=True,blank=True,default='')
    trailer = models.CharField(max_length=500, null=True,blank=True,default='')
    plan = models.CharField(max_length=10,default='')
    

    def __str__(self):
        return self.movie_name
    
    
class subscription_plan(models.Model):
    
    name = models.CharField(max_length=20)
    duration_day = models.IntegerField(default=0)
    support = models.CharField(max_length=30)
    amount = models.IntegerField(default=0)
    
    
class user_plan(models.Model):
    username = models.CharField(max_length=50,default='')
    plan_name = models.CharField(max_length=10,default='')
    