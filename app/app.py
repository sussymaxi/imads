from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import os
import asyncio  # Required for async functions
from models.users import User

# ------------------------------
# 🚀 FLASK APP CONFIGURATION
# ------------------------------

from config import Config
from json_outputs import main as fetch_json_outputs
from models.database import db

# Initialize the Flask app and other configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'imads')
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ------------------------------
# 📌 DATABASE SETUP
# ------------------------------
db = SQLAlchemy(app)

# ------------------------------
# 🔒 LOGIN CONFIGURATION
# ------------------------------
login_manager = LoginManager(app)
login_manager.login_view = "home"  # Redirects users to home if not authenticated

@login_manager.user_loader
def load_user(user_id):
    print("User ID:", user_id)
    with db.session as session:  # Use session context
        return session.get(User, int(user_id))
# ------------------------------
# 📜 FORMS
# ------------------------------
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken. Choose another.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered. Please log in.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

# ------------------------------
# 🌍 ROUTES
# ------------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    register_form = RegistrationForm()
    login_form = LoginForm()

    if register_form.validate_on_submit() and "register" in request.form:
        hashed_password = generate_password_hash(register_form.password.data, method="pbkdf2:sha256")
        new_user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        print("!!Ok")
        return redirect(url_for("home"))

    if login_form.validate_on_submit() and "login" in request.form:
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash("Logged in successfully!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Login failed. Check email and password.", "danger")

    return render_template("index.html", title="Imads - Amazon Discounts", register_form=register_form, login_form=login_form)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile", user=current_user)

# ------------------------------
# 🚀 JSON FETCH ROUTE
# ------------------------------

async def fetch_json_outputs(chat_name, limit):
    return {"messages": [{"id": i, "message": f"Sample message {i}"} for i in range(limit)]}

@app.route("/fetch-json")
def fetch_json():
    chat_name = "leofferteita"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(fetch_json_outputs(chat_name, 20))
    json_data = [{"id": result["id"], "message": result["message"]} for result in results["messages"]]
    loop.close()
    return jsonify(json_data)

# ------------------------------
# 🛠 DATABASE CREATION
# ------------------------------
# with app.app_context():
#     db.create_all()

# ------------------------------
# 🚀 RUN FLASK APP
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
