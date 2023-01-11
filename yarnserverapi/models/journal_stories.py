from django.db import models
from .my_journal import MyJournal
from .my_story import MyStory

class JournalStories(models.Model):
  
  my_journal_id = models.ForeignKey(MyJournal, on_delete=models.CASCADE)
  my_story_id = models.ForeignKey(MyStory, on_delete=models.CASCADE)
