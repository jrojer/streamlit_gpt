import base64
from pathlib import Path
from typing import Optional


class Image:
    def __init__(self, description: Optional[str] = None):
        self._image_data: bytes
        self._description = description

    @staticmethod
    def from_path(path: str | Path) -> "Image":
        newImage = Image()
        with open(path, "rb") as image_file:
            newImage._image_data = image_file.read()
        return newImage

    @staticmethod
    def from_bytes(buffer: bytes) -> "Image":
        newImage = Image()
        newImage._image_data = buffer
        return newImage

    @staticmethod
    def from_base64(base64_str: str) -> "Image":
        newImage = Image()
        newImage._image_data = base64.b64decode(base64_str)
        return newImage

    def as_base64(self) -> str:
        return base64.b64encode(self._image_data).decode("utf-8")

    def description(self) -> Optional[str]:
        return self._description
