from flask import Flask

app = Flask(__name__)
app.secret_key = 'maggimaggi'

import cookBook.views
import cookBook.datalayer.db
