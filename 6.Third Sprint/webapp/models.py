from django.db import models
# Create your models here.

class users(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	contact=models.CharField(max_length=100);
	pwd=models.CharField(max_length=100);
	addr=models.CharField(max_length=600);
	
class rooms(models.Model):
	roomnum=models.CharField(max_length=100);
	beds=models.IntegerField();
	available=models.IntegerField();

class Request(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	mode=models.CharField(max_length=100);
	stz=models.CharField(max_length=100);

class mbooking(models.Model):
	roomnum=models.CharField(max_length=100);
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	dat_e=models.CharField(max_length=100);
	amount=models.CharField(max_length=100);

class dbooking(models.Model):
	roomnum=models.CharField(max_length=100);
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	fdate=models.CharField(max_length=100);
	ldate=models.CharField(max_length=100);
	days=models.CharField(max_length=100);
	amount=models.CharField(max_length=100);

class srbooking(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	mode=models.CharField(max_length=100);
	dat_e=models.CharField(max_length=100);
	amount=models.CharField(max_length=100);

class transactions(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	room=models.CharField(max_length=100);
	dat_e=models.CharField(max_length=100);
	amount=models.CharField(max_length=100);
	stz=models.CharField(max_length=100);


class missing_items(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	contact=models.CharField(max_length=100);
	name_item=models.CharField(max_length=100);
	description=models.CharField(max_length=1000);
	image=models.CharField(max_length=500);
	stz=models.CharField(max_length=100);








