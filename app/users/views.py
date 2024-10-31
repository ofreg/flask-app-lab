from . import users_bp
from flask import render_template, abort, request, url_for,redirect, make_response, session
from datetime import datetime, timedelta
from flask import flash, Flask

@users_bp.route("hi/<string:name>")   #/hi/ivan?age=45&q=fdfdf
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   , Flask

    return render_template("hi.html",name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@users_bp.route("/profile")
def get_profile():
    if "username" in session:
        cookies = request.cookies  # Отримуємо куки
        username_value = session["username"]
        
        # Отримуємо кольорову схему з куків, значення за замовчуванням - 'light'
        color_scheme = request.cookies.get('color_scheme', 'light')  
        
        return render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme)  # Передаємо куки і кольорову схему
    flash("Сесія недійсна. Увійдіть знову.", "danger")
    return redirect(url_for("users.login"))


VALID_USERNAME = "user"
VALID_PASSWORD = "password123"
@users_bp.route("/login", methods=['GET','POST'])
def login():    
    if request.method == "POST":
        username = request.form["login"]
        password= request.form["password"]
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"]=username
            flash("Успішний вхід! Ласкаво просимо!", "success")
            return redirect(url_for('users.get_profile'))
        else:
            flash('Невірний логін або пароль', 'error')
    #session["age"]=30
    
    return render_template("login.html")

@users_bp.route("/logout")
def logout():
    session.pop('username', None)
    #session.pop('age', None)
    return redirect(url_for('users.get_profile'))
    
@users_bp.route("/set_cookie", methods=['POST'])
def set_cookie():
    key = request.form['key_cookie']  
    value = request.form['value_cookie']  
    max_age = int(request.form['time_cookie'])

    
    if not key:
        flash("Ключ кукі не може бути пустим!", "danger")
        return redirect(url_for('users.get_profile'))

    response = make_response(redirect(url_for('users.get_profile')))  
    response.set_cookie(key, value, max_age=max_age)  

    flash("Кука успішно встановлена!", "success") 
    return response


@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f'Користувач: {username}'  
    else:
        return 'Кука не знайдена'  
    
@users_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    key = request.form.get('value_delete_cookie')  
    response = make_response(redirect(url_for('users.get_profile')))
    if key and key in request.cookies:
        response.set_cookie(key, '', expires=0)  # Вказуємо шлях
        flash(f'Кука "{key}" видалена!', 'success')  
    else:
        flash(f'Кука "{key}" не існує або ключ не вказано!', 'danger')  

    return response


@users_bp.route('/delete_all_cookie', methods=['POST'])
def delete_all_cookie():
    response = make_response(redirect(url_for('users.get_profile')))
    for key in request.cookies.keys():
        response.set_cookie(key, '', expires=0)  

    flash('Всі куки видалені!', 'success') 

    return response

@users_bp.route("/set_color_scheme", methods=["POST"])
def set_color_scheme():
    scheme = request.form.get('color_scheme', 'light')  
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color_scheme', scheme)  
    return response

