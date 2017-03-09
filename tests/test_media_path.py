from werkzeug.datastructures import FileStorage

from .base import BaseTest
from flask_image_alchemy.fields import StdImageField
from flask_image_alchemy.storages import FileStorage as Storage
from sqlalchemy import Column, Integer

TEMP_IMAGES_DIR = 'tests/temp_images/'


class TestFieldUploadTo(BaseTest):

    TEST_DIR = "temp_images/avatars"

    def setUp(self):
        class App():
            config = {}
        app = App()
        app.config['MEDIA_PATH'] = 'tests/'
        self.file_storage = Storage()
        self.file_storage.init_app(app)
        super().setUp()

    def define_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            avatar = Column(
                StdImageField(
                    storage=self.file_storage,
                    upload_to=self.TEST_DIR
                ),
                nullable=False
            )
        self.User = User

    def test_create_instance(self):
        u = self.User()
        self.session.add(u)
        self.session.commit()

    def test_upload(self):
        with open(TEMP_IMAGES_DIR + 'python_logo.png', 'rb') as file:
            file = FileStorage(file)
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()
            self.assertTrue(self.TEST_DIR in u.avatar.url)

    def tearDown(self):
        for user in self.session.query(self.User):
            if user.avatar:
                user.avatar.delete(variations=True)
        super().tearDown()
