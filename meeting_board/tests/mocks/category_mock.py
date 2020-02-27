from api.models import Category


class CategoryMock:
    title = 'Test'

    def create_category_mock(self):
        return Category.objects.create()
