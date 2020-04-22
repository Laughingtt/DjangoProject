from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32)
    CHOICES = ((1, "Python"), (2, "Linux"), (3, "go"))
    category = models.IntegerField(choices=CHOICES)
    pub_time = models.DateField()
    publisher = models.ForeignKey(to="Publisher")
    authors = models.ManyToManyField(to="Author")


class Publisher(models.Model):
    title = models.CharField(max_length=32)


class Author(models.Model):
    name = models.CharField(max_length=32)


class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    token = models.UUIDField(null=True, blank=True)
    type = models.IntegerField(choices=((1, "普通用户"), (2, "vip"), (3, "svip")), default=1)
