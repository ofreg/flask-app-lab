from flask import request, redirect, url_for, render_template, abort, current_app
#from . import app
from app.users.views import users_bp
from flask_login import current_user
@current_app.route('/')
def main():
    return render_template("base.html")

@current_app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

#users

    
@current_app.route('/resume')
def resume():
    return render_template("resume.html")