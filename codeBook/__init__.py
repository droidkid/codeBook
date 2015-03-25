from flask import Flask

app = Flask(__name__)

import codeBook.views
import codeBook.db

