
from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', null=True, blank=True)
    users = models.ManyToManyField(User, related_name='badges')
    date_awarded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

