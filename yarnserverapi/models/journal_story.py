from django.db import models
from .my_journal import MyJournal
from .my_story import MyStory

class JournalStory(models.Model):

    my_journal = models.ForeignKey(MyJournal, on_delete=models.CASCADE)
    my_story = models.ForeignKey(MyStory, on_delete=models.CASCADE)
