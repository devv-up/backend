from django.urls import path

from meeting_board.services.meeting_board import MeetingBoard

urlpatterns: list = [
    path('board/', MeetingBoard.as_view(), name='board_create'),
]
