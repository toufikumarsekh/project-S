from flask import Flask, render_template, request, redirect
import os

from models.inquiry import db, Inquiry
from models.admin import Admin

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required
)

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

# ==================================================
# Database Configuration
# ==================================================

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ==================================================
# Flask Login Setup
# ==================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# ==================================================
# Create Tables
# ==================================================

with app.app_context():
    db.create_all()


# ==================================================
# Public Routes
# ==================================================

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/courses")
def courses():
    return render_template("courses.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/performances")
def performances():
    return render_template("performance.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        inquiry = Inquiry(
            name=request.form["name"],
            phone=request.form["phone"],
            email=request.form["email"],
            message=request.form["message"]
        )

        db.session.add(inquiry)
        db.session.commit()

        return redirect("/contact")

    return render_template("contact.html")


# ==================================================
# Authentication Routes
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:
            login_user(admin)
            return redirect("/admin")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# ==================================================
# Admin Dashboard
# ==================================================

@app.route("/admin")
@login_required
def admin():

    inquiries = Inquiry.query.order_by(
        Inquiry.created_at.desc()
    ).all()

    return render_template(
        "admin.html",
        inquiries=inquiries
    )


# ==================================================
# Run Application
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)