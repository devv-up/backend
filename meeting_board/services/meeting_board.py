import json

from rest_framework.response import Response
from rest_framework.views import APIView

from meeting_board.models import Board, Category
from meeting_board.serializers.board_serializers import BoardSerializer
from member.models import Member


class MeetingBoard(APIView):
    def post(self, request):
        request_body = json.loads(request.body.decode('utf-8'))

        board = Board.objects.create(
            title=request_body.get('title'),
            content=request_body.get('content'),
            location=request_body.get('location'),
            meeting_capacity=request_body.get('meetingCapacity'),
            meeting_date=request_body.get('meetingDate'),
            meeting_times_of_day=request_body.get('meetingTimesOfDay'),
            category=Category.objects.get(pk=request_body.get('categoryId')),
            author=Member.objects.get(id=request_body.get('authorId'))
        )

        return Response(BoardSerializer(board).data)
