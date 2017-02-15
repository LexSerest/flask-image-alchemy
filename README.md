Flask-ImageAlchemy
===============================
[![Build Status](https://travis-ci.org/rstit/flask-pyfcm.svg?branch=master)](https://travis-ci.org/rstit/flask-pyfcm)

version number: 0.0.1

Overview
--------

SQLAlchemy Standarized Image Field for Flask

Installation
--------------------

To install use pip:
```bash
$ pip install Flask-ImageAlchemy
```

Or clone the repo:
```bash
$ git clone https://github.com/rstit/flask-image-alchemy.git
$ python setup.py install
```
Usage
-----
Create model with StdImageField
```python
class User(db.Model):
    __tablename__ = 'example'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(
        StdImageField(
            storage=S3Storage(),
            variations={
                'thumbnail': {"width": 100, "height": 100, "crop": True}
            }
        ), nullable=True
    )
```
If you need S3Starage, set up config in your flask application:
```python
AWS_ACCESS_KEY_ID = "you-api-key"
AWS_SECRET_ACCESS_KEY = "you-secret-key"
AWS_REGION_NAME = "bucket-region"
S3_BUCKET_NAME = "bucket-name"
```

Then you can use image field
```python
u = User()
u.avatar = file
u.save()
```
And you have access to thumbnails:
```python
u.avatar.url
u.avatar.thumbnail
u.avatar.thumbnail.url
```


TODO
------------
* Validators (MinSizeValidator, MaxSizeValidator)
* Flask-Admin widget
* Coverage
* Docs Page