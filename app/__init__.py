from flask import Flask

app = Flask(__name__)
app.secret_key = 'bhs'  # 👈 Add this line

from app import routes

app.run(debug=True)