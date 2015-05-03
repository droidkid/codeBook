import os
from cookBook import app
if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000)); #get $PORT from heroku else default 5000
    app.run(host='0.0.0.0', port = port);

