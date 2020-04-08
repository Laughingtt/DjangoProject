from django.db import models

class Persons(models.Model):
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    birthday = models.DateField()
    time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'person'

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        # db_table = 'user'
        ordering = ['-id','date']

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey("User",on_delete=models.CASCADE)