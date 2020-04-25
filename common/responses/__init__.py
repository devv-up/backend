from rest_framework import status


class ResponseCollection:
    def __init__(self, status: int, message: str, detail: str = None):
        self.status = status
        self.message = message
        self.detail = detail

    def as_md(self) -> str:
        if self.detail is None:
            return f'{self.message}'
        return '\n\n%s\n\n```\n{\n\n\t"detail": "%s"\n\n}\n\n```' % \
               (self.message, self.detail)


APPLY_200_UPDATED = ResponseCollection(
    status=status.HTTP_200_OK,
    message='**Success**',
    detail='Successfully updated.'
)

APPLY_201_CREATED = ResponseCollection(
    status=status.HTTP_201_CREATED,
    message='**Success**',
    detail='Successfully created.'
)

APPLY_204_DELETED = ResponseCollection(
    status=status.HTTP_204_NO_CONTENT,
    message='**Success**',
)

APPLY_400_PARAMETER_ERROR = ResponseCollection(
    status=status.HTTP_400_BAD_REQUEST,
    message='Parameter Error',
    detail='An error message'
)

APPLY_404_NOT_FOUND = ResponseCollection(
    status=status.HTTP_404_NOT_FOUND,
    message='Not Found',
    detail='An error message'
)
