from flask import Flask
import codeBook.db

app = Flask(__name__)

import codeBook.views

