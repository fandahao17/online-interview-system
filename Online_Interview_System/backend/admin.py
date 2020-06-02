from django.contrib import admin
from . import models

admin.site.register(models.Applicant)
admin.site.register(models.Interviewer)
admin.site.register(models.Room)
# Register your models here.

