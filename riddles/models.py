from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Terminate(models.Model):
	over= models.BooleanField(default=False)

class Start(models.Model):
	start= models.BooleanField(default=False)

class Riddles(models.Model):
	text= models.CharField(max_length=100)

	def __str__(self):
		return self.text

class Info(models.Model):
	user= models.OneToOneField(User, related_name='foo')
	team_name= models.CharField(max_length=20)
	member1= models.CharField(max_length=20, default="Leader")
	member2= models.CharField(max_length=20)
	member3= models.CharField(max_length=20)
	member4= models.CharField(max_length=20, default="-")
	score= models.IntegerField(default=0)

	def __str__(self):
		return self.team_name

class Solution(models.Model):
	riddle= models.ForeignKey(Riddles)
	user= models.ForeignKey(User)
	image= models.FileField(null=True)
	description= models.CharField(max_length=150)
	correct= models.NullBooleanField(null=True, blank=True)
	submitted= models.BooleanField(default=False)

	def __str__(self):
		return self.description