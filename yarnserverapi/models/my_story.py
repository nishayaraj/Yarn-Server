from django.db import models
from .user import User

class myStory(models.Model):
  
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  author_name = models.CharField(max_length=50)
  is_published = models.BooleanField()
  public = models.BooleanField()
  story = models.TextField(max_length=900)
  date = models.DateField()
  