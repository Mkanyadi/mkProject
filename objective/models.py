from django.db import models
from django.contrib.auth.models import User

class Objective(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objectives')
    image = models.ImageField(upload_to='objectives/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, default="")
    with_who = models.CharField(max_length=255, blank=True)
    do_again = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(default=0)
    thoughts = models.TextField(blank=True, default="")

    memory_location = models.CharField(max_length=255, blank=True, default="")
    memory_with = models.CharField(max_length=255, blank=True, default="")
    memory_repeat = models.BooleanField(default=False)
    memory_rating = models.IntegerField(blank=True, null=True)
    memory_thoughts = models.TextField(blank=True, default="")
    memory_date = models.DateField(blank=True, null=True)

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

