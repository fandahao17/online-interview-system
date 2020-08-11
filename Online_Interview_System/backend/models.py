from django.db import models


class Hr(models.Model):
    '''Hr'''
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, default='11111111111')
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128, default='123456')
    # identity = models.IntegerField(default=3)

    class Meta:
        verbose_name = 'HR'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class hrToken(models.Model):
    name = models.OneToOneField(to='Hr', on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Hr_token'
        verbose_name_plural = verbose_name


class Interviewer(models.Model):
    '''interviewer'''
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, default='11111111111')
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128, default='123456')
    # identity = models.IntegerField(default=1)
    free1 = models.BooleanField(default=True)
    free2 = models.BooleanField(default=True)
    free3 = models.BooleanField(default=True)

    class Meta:
        verbose_name = '面试官'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Interviewee(models.Model):
    '''interviewee'''
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, default='11111111111')
    email = models.EmailField(primary_key=True)
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = '候选人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class interToken(models.Model):
    name = models.OneToOneField(to='Interviewer', on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Interviewer_token'
        verbose_name_plural = verbose_name


class Room(models.Model):
    '''room'''
    roomid = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    # exam = models.CharField(max_length=128)
    # tempeval = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tester = models.ForeignKey('Interviewer', on_delete=models.CASCADE)
    interviewee = models.ForeignKey('Interviewee', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = '面试房间'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.roomid)


class Super(models.Model):
	'''Superadmin'''
	name = models.CharField(max_length=128)
	mobile = models.CharField(max_length=20, default='11111111111')
	email = models.EmailField(primary_key=True)
	password = models.CharField(max_length=128, default='123456')
	# identity = models.IntegerField(default=2)

	class Meta:
		verbose_name = '超级管理员'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class superToken(models.Model):
    name = models.OneToOneField(to='Super', on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Super_token'
        verbose_name_plural = verbose_name
