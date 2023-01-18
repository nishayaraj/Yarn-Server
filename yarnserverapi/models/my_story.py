from django.db import models
from .user import User

class MyStory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    is_published = models.BooleanField()
    public = models.BooleanField()
    story = models.TextField(max_length=900)
    date = models.DateField()
    image_url = models.CharField(max_length=200)
  
    @property
    def journals_on_story(self):
        return self.__journals_on_story
    
    @journals_on_story.setter
    def journals_on_story(self, value):
        self.__journals_on_story=value
