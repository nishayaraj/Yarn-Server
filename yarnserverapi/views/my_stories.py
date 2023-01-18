"""View module for handling requests about game types"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from yarnserverapi.models import MyStory, User, MyJournal, JournalStory


class MyStoryView(ViewSet):
    """Yarn my story view

        Returns:
            Response -- JSON serialized Story data
        """

    def retrieve(self, request, pk):
        """ getting my story data by id
        """
        try:
            my_stories = MyStory.objects.get(pk=pk)

            serializer = MyStorySerializer(my_stories)
            serial_my_story = serializer.data
            serial_my_story['authorName'] = serial_my_story.pop('author_name')
            serial_my_story['imageUrl'] = serial_my_story.pop('image_url')
            serial_my_story['isPublished'] = serial_my_story.pop('is_published')
            serial_my_story['userId'] = serial_my_story.pop('user_id')

            filtered_journals_story = JournalStory.objects.filter(my_story_id=my_stories.id)
            journals_on_story = []

            for journal_story in filtered_journals_story:
                try:
                    journal_on_story = MyJournal.objects.get(id=journal_story.my_journal_id)

                    journals_on_story.append(journal_on_story.journal_type)
                except:
                    pass

            serial_my_story['journals'] = journals_on_story

            return Response(serial_my_story)
        except MyStory.DoesNotExist as ex:
            return Response({'message': 'Unable to fetch story data. '
                             + ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """get all stories"""
        my_stories = MyStory.objects.all()
        serializer = MyStorySerializer(my_stories, many=True)
        serial_my_story = serializer.data
        for my_story in serial_my_story:
            my_story['authorName'] = my_story.pop('author_name')
            my_story['imageUrl'] = my_story.pop('image_url')
            my_story['isPublished'] = my_story.pop('is_published')
            my_story['userId'] = my_story.pop('user_id')

            filtered_journals_story = JournalStory.objects.filter(my_story_id=my_story.pop('id'))
            journals_on_story = []

            for journal_story in filtered_journals_story:
                try:
                    journal_on_story = MyJournal.objects.get(id=journal_story.my_journal_id)

                    journals_on_story.append(journal_on_story.journal_type)
                except:
                    pass

            my_story['journals'] = journals_on_story

        return Response(serial_my_story)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """

        user_id = request.data['user_id']

        my_story = MyStory.objects.create(
            title=request.data['title'],
            author_name=request.data['author_name'],
            is_published=request.data['is_published'],
            public=request.data['public'],
            story=request.data['story'],
            date=request.data['date'],
            user_id = user_id,
            image_url=request.data['image_url']
        )

        #capture post tags from form and create them
        journals_ids = request.data['journals']

        journals = [MyJournal.objects.get(pk=journal_id) for journal_id in journals_ids]

        for journal in journals:
            journal_story = JournalStory(my_journal=journal, my_story=my_story)
            journal_story.save()

        serializer = MyStorySerializer(my_story)
        return Response(serializer.data)

class MyStorySerializer(serializers.ModelSerializer):
    """JSON serializer for stories
    """
    class Meta:
        model = MyStory
        fields = ('id', 'title', 'author_name',
                  'is_published', 'public', 'story', 'date',
                  'user_id', 'image_url', 'journals_on_story')
