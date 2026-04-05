from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('civil', 'Civil'),
        ('clubs', 'Clubs'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academic')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
