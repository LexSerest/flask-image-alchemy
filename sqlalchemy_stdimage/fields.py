import sqlalchemy.types as types

from sqlalchemy_stdimage.utils import process_thumbnail
from .storages import FileStorage

class StdImageField(types.TypeDecorator):

    impl = types.JSON

    def __init__(self, storage=FileStorage(), variations=None,
                 process_async=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = storage
        self.variations = variations
        self.process_async = process_async

    def process_bind_param(self, file, dialect):
        if file:
            self.storage.write(file.read(), "temp"+file.name.split("/")[1])
            if self.variations:
                process_thumbnail(file, self.variations, self.storage)
            return {
                "original": file.name
            }

    def process_result_value(self, value, dialect):
        return value.get("original")
