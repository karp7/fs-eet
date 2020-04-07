from django.db import models
from django.conf import settings

# Create your models here.



class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("John", 36)

class Project(models.Model):
    name = models.CharField(max_length=25, blank=True)
    description = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name



class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=settings.MEDIA_ROOT)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    prjog = models.ForeignKey(Project,on_delete=models.CASCADE)

    def __unicode__(self):
        return self.description