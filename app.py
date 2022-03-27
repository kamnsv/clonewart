from flask import render_template
  
def routes(app):

  @app.route('/')
  def hello_world():
      return render_template('index.html')   
