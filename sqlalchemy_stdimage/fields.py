import sqlalchemy.types as types

from sqlalchemy_stdimage.utils import process_thumbnail, validate_variations
from .storages import FileStorage, BaseStorage


class StdImageFile:
    def __init__(self, storage, json_data):
        self.storage = storage
        self.json_data = json_data
        self._set_attributes()

    def _set_attributes(self):
        setattr(self, "url", self.json_data.pop("original", None))
        for name, url in self.json_data.items():
            setattr(self, name, StdImageFile(self.storage, {"original": url}))


class StdImageField(types.TypeDecorator):

    impl = types.JSON

    def __init__(self, storage:BaseStorage=FileStorage(), variations:dict=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = storage
        self.variations = validate_variations(variations) if variations else None

    def process_bind_param(self, file, dialect):
        if file:
            self.storage.write(file.read(), "temp.png")
            data = {"original": file.name}
            if self.variations:
                values = process_thumbnail(file, self.variations, self.storage)
                data.update({key:value for key, value in values})
            return data

    def process_result_value(self, value, dialect):
        return StdImageFile(self.storage, value)
