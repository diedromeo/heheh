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

# Serve files from same directory (no static folder)
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #00FF00; 
                text-align: center; 
                font-family: 'Courier New', monospace; 
            }}
            h1 {{ font-size: 36px; margin-top: 60px; }}
            p {{ font-size: 18px; }}
            a {{ 
                color: #FF0000; font-size: 20px; text-decoration: none; border: 2px solid #FF0000; 
                padding: 10px 20px; display: inline-block; margin-top: 20px; background: rgba(0, 0, 0, 0.7); 
            }}
            a:hover {{ background: #FF0000; color: #000; }}
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #FFFFFF; text-align: center; font-family: 'Courier New', monospace; 
            }}
            h1 {{ color: #00FF00; font-size: 32px; }}
            .container {{ background: rgba(0, 0, 0, 0.8); padding: 30px; border: 2px solid #FF0000; display: inline-block; margin-top: 80px; }}
            input {{ padding: 10px; font-size: 16px; margin: 10px; width: 250px; border: 2px solid #FF0000; background: #000; color: #00FF00; text-align: center; font-family: 'Courier New', monospace; }}
            input[type="submit"] {{ border: 2px solid #00FF00; color: #000; background: #00FF00; cursor: pointer; width: 150px; }}
            input[type="submit"]:hover {{ background: #FF0000; border-color: #FF0000; color: #FFF; }}
            .error {{ color: #FF0000; font-size: 16px; font-weight: bold; }}
            .hint {{ font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔴🟢 SQUID GAME LOGIN 🔴🟢</h1>
            {"<p class='error'>" + error + "</p>" if error else ""}
            <form method="POST">
                <input type="text" name="username" placeholder="Username"><br>
                <input type="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Login">
            </form>
            <p class="hint">Hint: The system trusts your input...</p>
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #00FF00; text-align: center; font-family: 'Courier New', monospace; 
            }}
            h1 {{ font-size: 36px; margin-top: 50px; }}
            p {{ font-size: 20px; }}
            .flag {{ font-size: 18px; font-weight: bold; color: #FF0000; background: rgba(0, 0, 0, 0.8); padding: 8px; border: 2px solid #FF0000; }}
            img {{ margin: 20px 0; border: 2px solid #FF0000; max-width: 500px; }}
            a {{ color: #FF0000; font-size: 20px; text-decoration: none; border: 2px solid #FF0000; padding: 10px 20px; display: inline-block; margin-top: 20px; background: rgba(0, 0, 0, 0.7); }}
            a:hover {{ background: #FF0000; color: #000; }}
        </style>
    </head>
    <body>
        <h1>🏆 FRONT MAN: {session["user"]}</h1>
        <p>🎭 You’ve taken control!</p>
        <img src="{url_for('serve_file', filename='gg.gif')}" alt="Squid Game Victory">
        <p class="flag">🚩 FLAG: CyberX{{$quid_g4me_h4cked}} 🚩</p>
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

# Serve files from same directory (no static folder)
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #00FF00; 
                text-align: center; 
                font-family: 'Courier New', monospace; 
            }}
            h1 {{ font-size: 36px; margin-top: 60px; }}
            p {{ font-size: 18px; }}
            a {{ 
                color: #FF0000; font-size: 20px; text-decoration: none; border: 2px solid #FF0000; 
                padding: 10px 20px; display: inline-block; margin-top: 20px; background: rgba(0, 0, 0, 0.7); 
            }}
            a:hover {{ background: #FF0000; color: #000; }}
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #FFFFFF; text-align: center; font-family: 'Courier New', monospace; 
            }}
            h1 {{ color: #00FF00; font-size: 32px; }}
            .container {{ background: rgba(0, 0, 0, 0.8); padding: 30px; border: 2px solid #FF0000; display: inline-block; margin-top: 80px; }}
            input {{ padding: 10px; font-size: 16px; margin: 10px; width: 250px; border: 2px solid #FF0000; background: #000; color: #00FF00; text-align: center; font-family: 'Courier New', monospace; }}
            input[type="submit"] {{ border: 2px solid #00FF00; color: #000; background: #00FF00; cursor: pointer; width: 150px; }}
            input[type="submit"]:hover {{ background: #FF0000; border-color: #FF0000; color: #FFF; }}
            .error {{ color: #FF0000; font-size: 16px; font-weight: bold; }}
            .hint {{ font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔴🟢 SQUID GAME LOGIN 🔴🟢</h1>
            {"<p class='error'>" + error + "</p>" if error else ""}
            <form method="POST">
                <input type="text" name="username" placeholder="Username"><br>
                <input type="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Login">
            </form>
            <p class="hint">Hint: The system trusts your input...</p>
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
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{url_for('serve_file', filename='bg.webp')}') no-repeat center center fixed; 
                background-size: cover; 
                color: #00FF00; text-align: center; font-family: 'Courier New', monospace; 
            }}
            h1 {{ font-size: 36px; margin-top: 50px; }}
            p {{ font-size: 20px; }}
            .flag {{ font-size: 18px; font-weight: bold; color: #FF0000; background: rgba(0, 0, 0, 0.8); padding: 8px; border: 2px solid #FF0000; }}
            img {{ margin: 20px 0; border: 2px solid #FF0000; max-width: 500px; }}
            a {{ color: #FF0000; font-size: 20px; text-decoration: none; border: 2px solid #FF0000; padding: 10px 20px; display: inline-block; margin-top: 20px; background: rgba(0, 0, 0, 0.7); }}
            a:hover {{ background: #FF0000; color: #000; }}
        </style>
    </head>
    <body>
        <h1>🏆 FRONT MAN: {session["user"]}</h1>
        <p>🎭 You’ve taken control!</p>
        <img src="{url_for('serve_file', filename='gg.gif')}" alt="Squid Game Victory">
        <p class="flag">🚩 FLAG: CyberX{{$quid_g4me_h4cked}} 🚩</p>
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
