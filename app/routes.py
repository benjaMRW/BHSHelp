from app import app
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
import requests 
from bs4 import BeautifulSoup  
from datetime import datetime, time
import feedparser
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from webdriver_manager.chrome import ChromeDriverManager

# Initialize app and secret key
app.secret_key = 'school_project_123'  # Simple key for development

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "school.db")
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html', page_title='Home')


@app.route('/notices')
def notices():
    notices_data = get_school_notices()
    return render_template('notices.html', notices=notices_data)

def get_school_notices():
    try:
        feed = feedparser.parse("https://burnside.school.kiwi/rss")
        notices = []
        for entry in feed.entries[:10]:  # Get latest 10 notices
            notices.append({
                'title': entry.get('title', 'No title'),
                'date': entry.get('published', 'No date'),
                'content': entry.get('description', 'No content')
            })
        return notices
    except Exception as e:
        print(f"Error fetching notices: {str(e)}")
        return []



if __name__ == '__main__':
    app.run(debug=True)