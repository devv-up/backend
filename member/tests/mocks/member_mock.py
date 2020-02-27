from api.models import Member


class MemberMock:
    username = 'test123'
    email = 'test123@test.com'
    password = '1111'

    def create_member_mock(self):
        return Member.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
