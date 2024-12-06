from . import users_bp
from flask import render_template, abort, request, url_for,redirect, make_response, session,current_app
from datetime import datetime, timedelta
from flask import flash, Flask
from app import bcrypt
from app import db
from app.users.forms import RegistrationForm
from flask_bcrypt import check_password_hash
from app.users.models import User
from app.users.forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user, login_manager
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
        cookies = request.cookies  
        username_value = session["username"]
        
        # Отримуємо кольорову схему з куків, значення за замовчуванням - 'light'
        color_scheme = request.cookies.get('color_scheme', 'light')  
        
        return render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme)  
    flash("Сесія недійсна. Увійдіть знову.", "danger")
    return redirect(url_for("users.login"))


from app.users.models import User  
from app import db  
  

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Перевірка, чи користувач вже авторизований
        return redirect(url_for('users.account'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Успішний вхід!", "success")
            next_page = request.args.get('next')  # Для перенаправлення назад, якщо користувач неавторизований
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash("Невірний email або пароль.", "danger")
    return render_template("login.html", form=form)

@users_bp.route("/users_list")
def users_list():
    users = User.query.all()  # Отримуємо всіх користувачів з бази даних
    if not users:  # Перевірка, чи є користувачі в базі
        return render_template("users_list.html", message="Немає зареєстрованих користувачів")
    
    return render_template("users_list.html", users=users, count=len(users))
from flask_login import login_required, current_user
from flask import render_template, flash
@users_bp.route("/account")
@login_required
def account():
    # current_user надає доступ до поточного авторизованого користувача
    return render_template(
        "account.html",
        username=current_user.username,
        email=current_user.email
    )


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for('users.login'))

    
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
        response.set_cookie(key, '', expires=0)  
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




@users_bp.route("/register",methods=['GET','POST'])
def register():
    from app.users.models import User
    form = RegistrationForm()
    if form.validate_on_submit():
        username= form.username.data
        email=form.email.data
        password=form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created for {form.username.data}!',category='succes')
        return redirect(url_for('login'))
    return render_template('register.html',form=form, title='Register')