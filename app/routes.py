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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from webdriver_manager.chrome import ChromeDriverManager
import app.models as models

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "school.db")
db.init_app(app)
      




# basic route
@app.route('/')
def root():
    return render_template('home.html', page_title='HomePage')

@app.route('/subjects')
def subjects():
    return render_template('subjects.html', page_title='Subjects')





def login_to_burnside(email, password):
    try:
        # Configure Chrome (runs in background)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # No browser window pops up
        options.add_argument("--disable-gpu")
        
        # Automatic ChromeDriver setup
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get("https://burnside.school.kiwi/")

        # Wait for login form and fill credentials
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))  # CHANGE THIS SELECTOR
        ).send_keys(email)
        
        driver.find_element(By.ID, "password").send_keys(password)  # CHANGE THIS
        driver.find_element(By.ID, "login-button").click()  # CHANGE THIS

        # Wait for dashboard to load (check for a unique element)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))  # CHANGE THIS
        )

        # --- SCRAPE STUDENT DATA ---
        # Example: Fetch grades (customize selectors)
        grades = []
        grade_elements = driver.find_elements(By.CSS_SELECTOR, ".grade-item")  # CHANGE THIS
        for grade in grade_elements:
            grades.append(grade.text)

        # Example: Fetch attendance
        attendance = driver.find_element(By.CLASS_NAME, "attendance").text  # CHANGE THIS

        # Store data in Flask session
        session['logged_in'] = True
        session['email'] = email
        session['grades'] = grades
        session['attendance'] = attendance

        # Close browser
        driver.quit()

        # Redirect to student info page
        return redirect(url_for('student_info'))

    except Exception as e:
        print("Error:", e)
        return None  # Login failed

@app.route('/students')
def students():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template(
        'student.html',
        email=session['email'],
        grades=session.get('grades', []),
        attendance=session.get('attendance', 'No data')
    )

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