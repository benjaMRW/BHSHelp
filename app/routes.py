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
import folium
from folium.plugins import Search



# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "school.db")
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html', page_title='Home')

@app.route('/career')
def kol():
    return render_template('career.html', page_title='Home')

@app.route('/login')
def login():
    return render_template('login.html', page_title='Home')

@app.route('/student')
def students():
    return render_template('student.html', page_title='Home')

@app.route('/subjects')
def subjects():
    return render_template('subjects.html', page_title='Home')



@app.route('/map')
def map():
    start_name = request.args.get('start', '').strip().title()
    destination_name = request.args.get('destination', '').strip().title()

    SCHOOL_CENTER = [-43.50740156866357, 172.5766764229265]

    locations = {
        "A Block": [-43.50767607962358, 172.57621966007108],
        "B Block": [-43.507258002762555, 172.57649534465384],
        "C1 Block": [-43.507336958220584, 172.57692885310962],
        "C3-4 Block": [-43.50713855170288, 172.57701091063876],
        "P Block": [-43.50679524519272, 172.57576170047136],
        "M Block": [-43.508036322773854, 172.57585920976163],
        "Aurora Center": [-43.508548336966456, 172.57611858764898],
        "Library": [-43.50768093385897, 172.57690035175943],
        "G Block": [-43.50680754991145, 172.57687446294506],
        "L Block": [-43.50729540052514, 172.57605599645274],
        "N Block": [-43.50672110583437, 172.57630225157354],
        "E Block": [-43.50743157630898, 172.57557856325985],
        "K5-K6 Block": [-43.50599959130328, 172.5766635615753],
        "K1-K3 Block": [-43.5062665985537, 172.57640539896025],
        "Hunter Gym": [-43.50632638862487, 172.57709402902427],
        "Cross Gym": [-43.50673346447026, 172.57777757004496],
        "Dance Hall": [-43.50622379965693, 172.57682248245672],
        "Canteen": [-43.50739087991838, 172.57747902572711],
        "Pool": [-43.50698842492684, 172.57770103373863],
        "Turf/Football-Field": [-43.506852653812025, 172.57802912691722],
        "D1-D6 Block": [-43.50773718242374, 172.57730998413808],
        "D13-D16 Block": [-43.50761170681216, 172.57759832158754],
        "X Block": [-43.50696927145228, 172.57637389795957]
    }

    m = folium.Map(
        location=SCHOOL_CENTER,
        zoom_start=18,
        tiles='CartoDB positron',
        zoom_control=False,
        attributionControl=False
    )

    # Add all location markers
    for name, coords in locations.items():
        folium.Marker(
            location=coords,
            icon=folium.DivIcon(
                html=f"""<div style="font: bold 10px Arial; color: #333; text-shadow: 0 0 2px white;">{name}</div>"""
            )
        ).add_to(m)


    return render_template('map.html', map_html=m._repr_html_(), page_title='Campus Blocks')




@app.route('/notices')
def notices():
    notices_data = get_school_notices()
    return render_template('notices.html', notices=notices_data)

def get_school_notices():
    try:
        feed = feedparser.parse("https://burnside.school.kiwi/rss")
        notices = []
        for entry in feed.entries[:40]:  # Get latest 40 notices
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