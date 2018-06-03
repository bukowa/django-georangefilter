import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# custom settings for test
SETTINGS_DICT = dict(
    SECRET_KEY="asdasdsadasdasd",
    INSTALLED_APPS=["georangefilter", "tests"],  # todo
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "georangefilter",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "",
        }
    },
)
