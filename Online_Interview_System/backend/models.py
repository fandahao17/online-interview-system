from django.db import models

class Hr(models.Model):
    '''Hr'''
    name = models.CharField(max_length = 128)
    mobile = models.CharField(max_length = 20, default='11111111111')
    email = models.EmailField(primary_key = True)
    password = models.CharField(max_length = 128, default='123456')
    identity = models.IntegerField(default=3)

    class Meta:
        verbose_name = 'Hr_message'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class hrToken(models.Model):
    name = models.OneToOneField(to='Hr', on_delete = models.DO_NOTHING)
    token = models.CharField(max_length = 60)
    class Meta:
        verbose_name = 'Hr_token'
        verbose_name_plural = verbose_name

class Interviewer(models.Model):
    '''interviewer'''
    name = models.CharField(max_length = 128)
    mobile = models.CharField(max_length = 20, default='11111111111')
    email = models.EmailField(primary_key = True)
    password = models.CharField(max_length = 128, default='123456')
    identity = models.IntegerField(default = 1)
    free1 = models.DateTimeField(null=True,blank=True)
    free2 = models.DateTimeField(null=True,blank=True)
    free3 = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name = 'interviewer_message'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class interToken(models.Model):
    name = models.OneToOneField(to='Interviewer', on_delete = models.DO_NOTHING)
    token = models.CharField(max_length = 60)
    class Meta:
        verbose_name = 'Interviewer_token'
        verbose_name_plural = verbose_name

class Room(models.Model):
    '''room'''
    roomid = models.IntegerField()
    time = models.DateTimeField(null=True,blank=True)
    exam = models.CharField(max_length = 128)
    tempeval = models.CharField(max_length = 20)
    finaleval = models.CharField(max_length = 20)
    accept = models.IntegerField()
    record = models.CharField(max_length = 128)
    tester = models.ForeignKey('Interviewer', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'metting_room_message'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.roomid

class Super(models.Model):
	'''Superadmin'''
	name = models.CharField(max_length = 128)
	mobile = models.CharField(max_length = 20, default='11111111111')
	email = models.EmailField(primary_key = True)
	password = models.CharField(max_length = 128, default='123456')
	identity = models.IntegerField(default=2) 
	
	class Meta:
		verbose_name = 'Superadmin_message'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

class superToken(models.Model):
    name = models.OneToOneField(to='Super', on_delete = models.DO_NOTHING)
    token = models.CharField(max_length = 60)
    class Meta:
        verbose_name = 'Super_token'
        verbose_name_plural = verbose_name
