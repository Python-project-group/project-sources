from django.db import models


# Create your models here.

class Person(models.Model):
    telNum = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    type = models.CharField(max_length=16)


class Company(models.Model):
    telNum = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=16, unique=True)
    address = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    type = models.CharField(max_length=16)
