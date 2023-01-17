"""View module for handling requests about game types"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from yarnserverapi.models import MyJournal, User


class MyJournalView(ViewSet):
    """Yarn my journal view

        Returns:
            Response -- JSON serialized Journal data
        """

    def retrieve(self, request, pk):
        """ getting my journal data by id
        """
        try:
            my_journals = MyJournal.objects.get(pk=pk)

            serializer = MyJournalSerializer(my_journals)
            serial_my_journal = serializer.data
            serial_my_journal['journalType'] = serial_my_journal.pop('journal_type')
            serial_my_journal['imageUrl'] = serial_my_journal.pop('image_url')
            serial_my_journal['userId'] = serial_my_journal.pop('user_id')

            return Response(serial_my_journal)
        except MyJournal.DoesNotExist as ex:
            return Response({'message': 'Unable to fetch journal data. '
                             + ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """get all journals"""
        my_journals = MyJournal.objects.all()
        serializer = MyJournalSerializer(my_journals, many=True)
        serial_my_journal = serializer.data
        for my_journal in serial_my_journal:
            my_journal['journalType'] = my_journal.pop('journal_type')
            my_journal['imageUrl'] = my_journal.pop('image_url')
            my_journal['userId'] = my_journal.pop('user_id')
        return Response(serial_my_journal)

    def create(self, request):
        '''handels creation of my journals'''
        user_id = request.data['user_id']

        try:
            User.objects.get(id = user_id)
            my_journal = MyJournal.objects.create(
            journal_type = request.data['journal_type'],
            image_url = request.data['image_url'],
            date = request.data['date'],
            user_id = user_id
            )

            serializer = MyJournalSerializer(my_journal)

            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': 'Unable to create journal. '
                             + ex.args[0]}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        """Handle PUT requests for my_journal

        Returns:
        Response -- Empty body with 204 status code
        """

        my_journal = MyJournal.objects.get(pk=pk)
        my_journal.journal_type = request.data['journal_type']
        my_journal.image_url = request.data['image_url']
        my_journal.date = request.data['date']

        my_journal.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class MyJournalSerializer(serializers.ModelSerializer):
    """JSON serializer for journals
    """
    class Meta:
        model = MyJournal
        fields = ('id', 'journal_type', 'image_url', 'date', 'user_id')
