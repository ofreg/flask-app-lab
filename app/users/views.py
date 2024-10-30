from . import users_bp
from flask import render_template, abort, request, url_for,redirect, make_response, session
from datetime import datetime, timedelta
from flask import flash
@users_bp.route("hi/<string:name>")   #/hi/ivan?age=45&q=fdfdf
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html",name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@users_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value= session["username"]
        return render_template("profile.html", username=username_value)
    flash("Invalid: Session.", "danger")
    return redirect(url_for("users.login"))

@users_bp.route("/login", methods=['GET','POST'])
def login():    
    if request.method == "POST":
        username = request.form["login"]
        session["username"]=username
        flash("Success: session added successfully.", "success")
        return redirect(url_for('users.get_profile'))
    #session["age"]=30
    
    return render_template("login.html")

@users_bp.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('users.get_profile'))
    

@users_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', expires=datetime.now()+timedelta(seconds=10))
    response.set_cookie('username', 'student', max_age=timedelta(seconds=10))
    return response

@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@users_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response
