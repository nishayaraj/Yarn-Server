"""View module for handling requests about game types"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from yarnserverapi.models import MyStory, MyJournal, JournalStory


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
                    journals_on_story.append({'id': journal_on_story.id, 'journalType': journal_on_story.journal_type})
                except:
                    pass

            serial_my_story['journals'] = journals_on_story

            return Response(serial_my_story)
        except MyStory.DoesNotExist as ex:
            return Response({'message': 'Unable to fetch story data. '
                             + ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """get my stories"""

        try:
            user_id = request.GET.get("userId")
            journal_id = request.GET.get("journalId")
            if not user_id and not journal_id:
                my_stories = MyStory.objects.filter(is_published=True, public=True).values()
                serializer = MyStorySerializer(my_stories, many=True)
                serial_my_story = serializer.data
                for my_story in serial_my_story:
                    my_story['authorName'] = my_story.pop('author_name')
                    my_story['imageUrl'] = my_story.pop('image_url')
                    my_story['isPublished'] = my_story.pop('is_published')
                    my_story['userId'] = my_story.pop('user_id')

                    filtered_journals_story = JournalStory.objects.filter(my_story_id=my_story['id'])
                    journals_on_story = []

                    for journal_story in filtered_journals_story:
                        try:
                            journal_on_story = MyJournal.objects.get(id=journal_story.my_journal_id)

                            journals_on_story.append({'id': journal_on_story.id, 'journalType': journal_on_story.journal_type})
                        except:
                            pass

                    my_story['journals'] = journals_on_story

                return Response(serial_my_story)
            if user_id:
                my_stories = MyStory.objects.filter(user_id=user_id).values()
                serializer = MyStorySerializer(my_stories, many=True)
                serial_my_story = serializer.data
                for my_story in serial_my_story:
                    my_story['authorName'] = my_story.pop('author_name')
                    my_story['imageUrl'] = my_story.pop('image_url')
                    my_story['isPublished'] = my_story.pop('is_published')
                    my_story['userId'] = my_story.pop('user_id')

                    filtered_journals_story = JournalStory.objects.filter(my_story_id=my_story['id'])
                    journals_on_story = []

                    for journal_story in filtered_journals_story:
                        try:
                            journal_on_story = MyJournal.objects.get(id=journal_story.my_journal_id)

                            journals_on_story.append({'id': journal_on_story.id, 'journalType': journal_on_story.journal_type})
                        except:
                            pass

                    my_story['journals'] = journals_on_story

                return Response(serial_my_story)
            if journal_id:
                storys_on_journal = []
                story_ids_with_journal_id = JournalStory.objects.filter(my_journal_id=journal_id)
                story_ids_with_journal_id_serializer = JournalStorySerializer(story_ids_with_journal_id, many=True)
                story_ids_with_journal_id_serializer_data = story_ids_with_journal_id_serializer.data
                for story_in_serializer_data in story_ids_with_journal_id_serializer_data:
                    try:
                        stories_in_data = MyStory.objects.get(id=story_in_serializer_data['my_story_id'])
                        stories_in_data_serializer = MyStorySerializer(stories_in_data)
                        my_story = stories_in_data_serializer.data
                        my_story['authorName'] = my_story.pop('author_name')
                        my_story['imageUrl'] = my_story.pop('image_url')
                        my_story['isPublished'] = my_story.pop('is_published')
                        my_story['userId'] = my_story.pop('user_id')

                        journals_story_id_filter = JournalStory.objects.filter(my_story_id=story_in_serializer_data['my_story_id'])
                        journals_story_id_filter_serializer = JournalStorySerializer(journals_story_id_filter, many=True)
                        journals_story_id_filter_serializer_data = journals_story_id_filter_serializer.data
                        journals_on_story = []
                        for journals_in_story in journals_story_id_filter_serializer_data:
                            try:
                                journal = MyJournal.objects.get(id=journals_in_story['my_journal_id'])
                                journals_on_story.append({'id': journal.id, 'journalType': journal.journal_type})
                            except:
                                pass

                        my_story['journals'] = journals_on_story
                        storys_on_journal.append(my_story)
                    except:
                        pass
            return Response(storys_on_journal)

        except MyStory.DoesNotExist as ex:
            return Response({'message': 'Unable to get my stories data. '
                             + ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """

        user_id = request.data['userId']

        my_story = MyStory.objects.create(
            title=request.data['title'],
            author_name=request.data['authorName'],
            is_published=request.data['isPublished'],
            public=request.data['public'],
            story=request.data['story'],
            date=request.data['date'],
            user_id = user_id,
            image_url=request.data['imageUrl']
        )

        #capture journal types from form and create them
        journals_ids = request.data['journals']

        journals = [MyJournal.objects.get(pk=journal_id) for journal_id in journals_ids]

        for journal in journals:
            journal_story = JournalStory(my_journal=journal, my_story=my_story)
            journal_story.save()

        serializer = MyStorySerializer(my_story)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for my_stories

        Returns:
        Response -- Empty body with 204 status code
        """
        try:
            my_story = MyStory.objects.get(pk=pk)
            my_story.title = request.data['title']
            my_story.author_name = request.data['authorName']
            my_story.is_published = request.data['isPublished']
            my_story.public = request.data['public']
            my_story.story = request.data['story']
            my_story.image_url = request.data['imageUrl']
            my_story.date = request.data['date']

            #capture journal types from form and create them
            journals_ids = request.data['journals']

            journals = [MyJournal.objects.get(pk=journal_id) for journal_id in journals_ids]

            existing_journals_story = JournalStory.objects.filter(my_story_id=pk)
            existing_journals_story.delete()

            for journal in journals:
                journal_story = JournalStory(my_journal=journal, my_story=my_story)
                journal_story.save()

            my_story.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except MyStory.DoesNotExist as ex:
            return Response({'message': 'Unable to update story data. '
                             + ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        '''Delete request for my_story'''
        try:
            my_story = MyStory.objects.get(pk=pk)
            my_story.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except MyStory.DoesNotExist as ex:
            return Response({'message': 'Unable to delete story data. '
                             + ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class MyStorySerializer(serializers.ModelSerializer):
    """JSON serializer for stories
    """
    class Meta:
        model = MyStory
        fields = ('id', 'title', 'author_name',
                  'is_published', 'public', 'story', 'date',
                  'user_id', 'image_url', 'journals_on_story')

class JournalStorySerializer(serializers.ModelSerializer):
    """JSON serializer for stories
    """
    class Meta:
        model = JournalStory
        fields = ('id', 'my_journal_id', 'my_story_id')
