from app import app
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy  # no more boring old SQL for us!
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "school.db")
db.init_app(app)
      

import app.models as models


# basic route
@app.route('/')
def root():
    return render_template('home.html', page_title='HomePage')

@app.route('/subject')
def subjects():
    return render_template('subjects.html', page_title='Subjects')


# @app.route('/map')
# def root():
#     return render_template('map.html', page_title='BHSmap')

# @app.route('/notices')
# def root():
#     return render_template('notices.html')

# @app.route('/teacher_finder')
# def root():
#     return render_template('teacher_finder.html')





@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
   app.run(debug=True)