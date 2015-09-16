#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 yuvaraj <yuvaraj@eee-pc>
#
# Distributed under terms of the MIT license.
import psycopg2
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


@app.teardown_appcontext
def close_get_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
