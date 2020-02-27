import json

from rest_framework.test import APITestCase

from api.tests.mocks.board_posting_data import BoardPostingData
from api.tests.mocks.category_mock import CategoryMock
from api.tests.mocks.member_mock import MemberMock


class MeetingBoardTest(APITestCase, MemberMock, CategoryMock, BoardPostingData):

    def test_board_creating(self):
        member = self.create_member_mock()
        category = self.create_category_mock()

        data = json.dumps({
            'title': self.title,
            'content': self.content,
            'location': self.location,
            'meetingCapacity': self.meeting_capacity,
            'meetingDate': self.meeting_date,
            'meetingTimesOfDay': self.meeting_times_of_day,
            'authorId': member.id,
            'categoryId': category.id
        })

        result = self.client.post('/board/', data, content_type='application/json')

        self.assertEquals(result.status_code, 200)
        self.assertEquals(result.data['title'], self.title)
        self.assertEquals(result.data['content'], self.content)
        self.assertEquals(result.data['location'], self.location)
        self.assertEquals(result.data['meetingCapacity'], self.meeting_capacity)
        self.assertEquals(result.data['meetingDate'], self.meeting_date)
        self.assertEquals(result.data['meetingTimesOfDay'], self.meeting_times_of_day)
        self.assertEquals(result.data['authorId'], member.id)
        self.assertEquals(result.data['categoryId'], category.id)
