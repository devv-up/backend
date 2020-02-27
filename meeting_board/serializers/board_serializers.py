from rest_framework import serializers

from meeting_board.models import Board


class BoardSerializer(serializers.ModelSerializer):
    meetingCapacity = serializers.IntegerField(source='meeting_capacity')
    meetingDate = serializers.DateTimeField(source='meeting_date')
    meetingTimesOfDay = serializers.IntegerField(source='meeting_times_of_day')
    authorId = serializers.IntegerField(source='author.id')
    categoryId = serializers.IntegerField(source='category.id')

    class Meta:
        model = Board
        fields = ('id', 'title', 'content', 'created_date', 'location'
                  'meetingCapacity', 'meetingDate', 'meetingTimesOfDay',
                  'categoryId', 'authorId',)
