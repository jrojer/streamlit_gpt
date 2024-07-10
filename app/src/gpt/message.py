from app.src.gpt.content_type import ContentType
from app.src.gpt.image import Image


class Message:
    def __init__(self, role: str, content: str, content_type: ContentType):
        self._role = role
        self._content = content
        self._content_type = content_type

    def role(self) -> str:
        return self._role

    def content(self) -> str:
        return self._content

    def content_type(self) -> ContentType:
        return self._content_type


def image_message(image: Image) -> Message:
    return Message("user", image.as_base64(), ContentType.Image)


def user_message(content: str) -> Message:
    return Message("user", content, ContentType.Text)


def assistant_message(content: str) -> Message:
    return Message("assistant", content, ContentType.Text)
