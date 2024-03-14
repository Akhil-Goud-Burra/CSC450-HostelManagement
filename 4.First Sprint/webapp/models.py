from django.db import models
# Create your models here.

class users(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	contact=models.CharField(max_length=100);
	pwd=models.CharField(max_length=100);
	addr=models.CharField(max_length=600);

'''
class rooms(models.Model):
	roomnum=models.CharField(max_length=100);
	beds=models.IntegerField();
	available=models.IntegerField();
'''