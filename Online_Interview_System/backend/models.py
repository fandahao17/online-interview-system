from django.db import models

class Applicant(models.Model):
    '''applicant'''
    name = models.CharField(max_length = 128)
    mobile = models.CharField(max_length = 20, unique = True)
    email = models.EmailField(primary_key = True, unique = True)
    status = models.IntegerField()
    image = models.ImageField(upload_to = 'image/%Y%m', default = 'image/default.jpg', max_length = 100)

    class Meta:
        verbose_name = 'applicant_message'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Interviewer(models.Model):
    '''interviewer'''
    name = models.CharField(max_length = 128)
    email = models.EmailField(primary_key = True, unique = True)
    free1 = models.DateTimeField(null=True,blank=True)
    free2 = models.DateTimeField(null=True,blank=True)
    free3 = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name = 'interviewer_message'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Room(models.Model):
    '''room'''
    roomid = models.IntegerField()
    time = models.DateTimeField(null=True,blank=True)
    exam = models.CharField(max_length = 128)
    tempeval = models.CharField(max_length = 20)
    finaleval = models.CharField(max_length = 20)
    accept = models.IntegerField()
    record = models.CharField(max_length = 128)
    applyer = models.ForeignKey('Applicant', on_delete = models.CASCADE)
    tester = models.ForeignKey('Interviewer', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'metting_room_message'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.roomid

