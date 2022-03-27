import sys
sys.path.remove('/usr/lib/python3/dist-packages')
sys.path.append('/home/c/cu99893/myenv/lib/python3.6/site-packages')
sys.path.append('/home/c/cu99893/clonewar')

from flask import Flask
app = Flask(__name__, template_folder='/home/c/cu99893/clonewar/templates')
application = app

from app import routes
routes(app)

if __name__ == '__main__':
    app.run()