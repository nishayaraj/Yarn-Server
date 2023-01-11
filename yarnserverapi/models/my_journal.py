from django.db import models
from .user import User

class MyJournal(models.Model):
  
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  journal_type = models.CharField(max_length=50)
  image_url = models.CharField(max_length=200)
  date = models.DateField()
