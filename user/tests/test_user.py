import pytest

from user.models import User


def signup(username, password):
    try:
        User.objects.create_user(username=username, password=password)
    except Exception as e:
        return 400
    return 200


@pytest.mark.django_db
def test_signup():
    """
    정상적으로 회원가입을 하는지 체크하는 테스트
    - 현재 작업중
    - 추가로 필요한 작업:
        - 입력 값의 유효성 테스트
        - test에 있는 함수를 views로 옮기고 url 연결하고 테스트
            (이 과정에서 status_code를 하드코딩에서 실제 값이 나오도록 만들기
        - jwt를 적용하고 현재의 signup()에는 jwt이 없어도 접근할 수 있도록 설정
    :return: 200 (status_code)
    """
    username = 'username'
    password = '1111'
    result = signup(username, password)
    assert result == 200


@pytest.mark.django_db
def test_signup_twice():
    """
    같은 정보로 회원가입을 2번 했을 때 오류를 리턴하는 테스트
    :return: 400 (status_code)
    """
    username = 'username'
    password = '1111'
    result = signup(username, password)
    result2 = signup(username, password)
    assert result2 == 400
