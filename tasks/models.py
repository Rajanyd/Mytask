from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    passcode = models.CharField(max_length=128)
    email = models.EmailField(unique=True,default= 'example@example.com')


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    category = models.CharField(max_length=100, blank=True, null=True)
