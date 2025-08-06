from flask import Flask, request, redirect, session, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

# Initialize Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///squidgame.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Serve files from the same directory as app.py
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="frontman").first():
        db.session.add(User(username="frontman", password="supersecure"))
        db.session.commit()

# Home Route
@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>Squid Game - Restricted Zone</title>
        <style>
            body {{ 
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                            url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #00FF00; 
                text-align: center; 
                font-family: 'Courier New', monospace; 
            }}
        </style>
    </head>
    <body>
        <h1>🔴🟢 SQUID GAME: RESTRICTED ACCESS 🔴🟢</h1>
        <p>Authorized personnel only.</p>
        <a href='/login'>[ Enter the Game ]</a>
    </body>
    </html>
    """

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        query = text(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
        result = db.session.execute(query).fetchone()
        if result:
            session["user"] = username
            return redirect("/dashboard")
        else:
            error = "🚨 Access Denied! Invalid credentials! 🚨"

    return f"""
    <html>
    <head>
        <title>Squid Game - Login</title>
        <style>
            body {{ 
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                            url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #FFFFFF; 
                text-align: center; 
            }}
        </style>
    </head>
    <body>
        <div>
            <h1>🔴🟢 SQUID GAME LOGIN 🔴🟢</h1>
            {"<p style='color:red;'>" + error + "</p>" if error else ""}
            <form method="POST">
                <input type="text" name="username" placeholder="Username"><br>
                <input type="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Login">
            </form>
        </div>
    </body>
    </html>
    """

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return f"""
    <html>
    <head>
        <title>Squid Game - Front Man</title>
        <style>
            body {{ 
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                            url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #00FF00; 
                text-align: center; 
            }}
        </style>
    </head>
    <body>
        <h1>🏆 FRONT MAN: {session["user"]}</h1>
        <p>🎭 You’ve taken control!</p>
        <img src="{url_for('serve_file', filename='gg.gif')}" alt="Squid Game Victory">
        <p>🚩 FLAG: ctf7{{$quid_g4me_h4cked}} 🚩</p>
        <a href='/logout'>[ Logout ]</a>
    </body>
    </html>
    """

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# Run the App
if __name__ == "__main__":
    app.run(debug=True)
