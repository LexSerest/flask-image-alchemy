from flask_image_alchemy.storages import S3Storage
from .base import BaseTest
from flask_image_alchemy.fields import StdImageField, StdImageFile
from sqlalchemy import Column, Integer

TEMP_IMAGES_DIR = 'temp_images/'
AWS_ACCESS_KEY = 'xxx'
AWS_SECRET = 'xxx'
AWS_REGION_NAME = 'eu-central-1'
BUCKET_NAME = ''


class TestS3Storage(BaseTest):

    def setUp(self):
        class App():
            config = {}
        app = App()
        app.config['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY
        app.config['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET
        app.config['AWS_REGION_NAME'] = AWS_REGION_NAME
        app.config['S3_BUCKET_NAME'] = BUCKET_NAME
        self.s3_storage = S3Storage()
        self.s3_storage.init_app(app)
        super().setUp()

    def define_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            id = Column(Integer, primary_key=True)
            avatar = Column(
                StdImageField(
                    storage=self.s3_storage,
                    variations={"thumbnail": {'height': 100, 'width': 100}}
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
            u = self.User()
            u.avatar = file
            self.session.add(u)
            self.session.commit()
            self.assertIsInstance(u.avatar, StdImageFile)
            self.assertIsNotNone(u.avatar.url)
            self.assertIsInstance(u.avatar.thumbnail, StdImageFile)
            self.assertIsNotNone(u.avatar.thumbnail.url)

    def tearDown(self):
        for user in self.session.query(self.User):
            if user.avatar:
                user.avatar.delete(variations=True)
        super().tearDown()
