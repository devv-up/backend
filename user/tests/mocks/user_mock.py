from user.models import User


class UserMock:
    username = 'test123'
    email = 'test123@test.com'
    password = '1111'

    def create_user_mock(self):
        return User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
