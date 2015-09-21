import psycopg2
import cloudinary
from flask import g

from cookBook import app
from config import *


def connectDB():
    return psycopg2.connect(database=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connectDB()
    return db


def get_cloudinary():
    cloudinary_config = getattr(g, '_cloudinary', None)
    if cloudinary_config is None:
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET)
        g._cloudinary = cloudinary
    return cloudinary


@app.teardown_appcontext
def close_get_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
