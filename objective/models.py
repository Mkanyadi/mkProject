from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Objective(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objectives')
    image = models.ImageField(upload_to='objectives/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)  # ← AICI
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Badge: {self.name} - User: {self.user.username}"