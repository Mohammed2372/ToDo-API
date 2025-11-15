from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    class Meta:
        ordering = ["-date_created"]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
