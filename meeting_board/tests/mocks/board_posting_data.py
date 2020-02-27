import time


class BoardPostingData:
    title = 'test_title'
    content = 'test_content'
    location = 'test_location'
    meeting_capacity = 10
    meeting_date = time.strftime('%Y-%m-%d', time.localtime())
    meeting_times_of_day = 1
