from app import app
from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from .models import Session, Person
from flask_sqlalchemy import SQLAlchemy  # no more boring old SQL for us!
import os
import requests 
from bs4 import BeautifulSoup  
from datetime import time
import feedparser
import pytz

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "school.db")
db.init_app(app)
      

import app.models as models


# basic route
@app.route('/')
def root():
    return render_template('home.html', page_title='HomePage')

@app.route('/subjects')
def subjects():
    return render_template('subjects.html', page_title='Subjects')





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Safely get the values from the form
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please fill in both fields.")
            return render_template('LogIn.html')

        # Now email and password are defined
        result = login_to_burnside(email, password)

        if result:
            return result  # You can also render_template here with the info
        else:
            flash("Login to Burnside website failed.")
            return render_template('LogIn.html')

    return render_template('LogIn.html')






# ... (keep your existing login and other routes)

@app.route('/notices')
def notices():
    try:
        # Method 1: Use feedparser (most reliable)
        feed = feedparser.parse("https://burnside.school.kiwi/rss")
        notices = []
        
        if feed.entries:
            for entry in feed.entries:
                description = entry.get('description', '')
                description = description.replace('KhR', '').replace('<![CDATA[', '').replace(']]>', '')
                
                notices.append({
                    "title": entry.get('title', 'No title'),
                    "link": entry.get('link', '#'),
                    "description": description,
                    "pubDate": entry.get('published', 'No date'),
                    "category": entry.get('tags', [{}])[0].get('term', 'General') if entry.get('tags') else 'General'
                })
        
        # Method 2: Fallback to BeautifulSoup
        if not notices:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get("https://burnside.school.kiwi/rss", headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                for item in soup.find_all('item'):
                    description = item.description.text if item.description else ""
                    notices.append({
                        "title": item.title.text if item.title else "No title",
                        "link": item.link.text if item.link else "#",
                        "description": description.replace('KhR', '').strip(),
                        "pubDate": item.pubDate.text if item.pubDate else "No date",
                        "category": item.category.text if item.category else "General"
                    })
        
        # Process dates for all notices
        for notice in notices:
            if notice['pubDate'] != 'No date':
                try:
                    # Parse with timezone
                    dt = datetime.strptime(notice['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
                    # Convert to NZ timezone
                    nz_time = dt.astimezone(pytz.timezone('Pacific/Auckland'))
                    # Format as: "Day, Date Month Year at Time (NZST)"
                    notice['pubDate'] = nz_time.strftime('%a, %d %b %Y at %I:%M %p (NZST)')
                except Exception as e:
                    print(f"Date formatting error: {e}")
                    notice['pubDate'] = notice['pubDate'].replace('+1200', ' (NZ Time)')
        
        return render_template('notices.html', notices=notices, page_title='School Notices')
            
    except Exception as e:
        print(f"Error: {e}")
        return render_template('notices.html', notices=[], page_title='School Notices', error="Temporarily unable to load notices")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
   app.run(debug=True)