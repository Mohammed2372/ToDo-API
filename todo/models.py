from django.db import models


# Create your models here.
class Todo(models.Model):
    class Meta:
        ordering = ["-date_created"]

    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
