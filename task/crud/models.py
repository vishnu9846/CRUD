from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

choice=(
    ('high','medium','low')
)
class Registration(models.Model):
    username=models.CharField(max_length=225)
    email = models.EmailField(max_length=254)
    password = models.CharField( max_length=50)
    confirmpassword = models.CharField( max_length=50)
    


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    task_name = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    assignee = models.CharField(max_length=100)
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
 