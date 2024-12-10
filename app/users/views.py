from . import users_bp
from flask import render_template, abort, request, url_for,redirect, make_response, session, current_app
from datetime import datetime, timedelta
from flask import flash, Flask
from app import bcrypt
from app import db
from app.users.forms import RegistrationForm
from flask_bcrypt import check_password_hash, generate_password_hash
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
#@current_app.route('/users')
#def account_detailis():
#    form = UpdateAccountForm()  # Ініціалізуємо форму
#    return render_template('account.html', username=current_user.username, email=current_user.email, form=form)


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

from datetime import datetime
import pytz
from app.users.forms import ChangePasswordForm, UpdateAccountForm
@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()  # Ініціалізуємо форму зміни пароля

    # Оновлення часу останнього входу
    current_user.last_seen = datetime.now(pytz.utc)  # Оновлюємо час останнього входу в UTC
    db.session.commit()  # Зберігаємо зміни в базі

    # Обробка форми на відправку
    if form.validate_on_submit():
        if form.picture.data:  # Перевірка, чи є завантажене зображення
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Оновлення полів користувача
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Ваш обліковий запис було успішно оновлено!', 'success')
        return redirect(url_for('users.account'))

    # Обробка зміни пароля
    if change_password_form.validate_on_submit():
        if not check_password_hash(current_user.password, change_password_form.old_password.data):
            flash('Невірний старий пароль.', 'danger')
        else:
            current_user.password = generate_password_hash(change_password_form.new_password.data)
            db.session.commit()
            flash('Ваш пароль було успішно змінено!', 'success')
            return redirect(url_for('users.account'))

    # Попереднє заповнення форми поточними даними
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me

    # Оновлення та відображення часу останнього входу
    if current_user.last_seen:
        if current_user.last_seen.tzinfo is None:
            last_seen_utc = current_user.last_seen.replace(tzinfo=pytz.utc)
        else:
            last_seen_utc = current_user.last_seen

        local_tz = pytz.timezone('Africa/Blantyre')  # Часова зона UTC+2
        last_seen_local = last_seen_utc.astimezone(local_tz)
        formatted_time = last_seen_local.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_time = 'Час не визначено'

    # Зображення профілю
    image_file = url_for('static', filename='profile_pics/' + (current_user.image_file if current_user.image_file else 'logo.jpg'))

    return render_template('account.html', title='Account', image_file=image_file, form=form, last_seen=formatted_time, change_password_form=change_password_form)
from app.users.forms import UpdateAccountForm
@users_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        # Оновлення даних профілю користувача
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        # Завантаження нового фото профілю
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # Реалізуйте `save_picture`
            current_user.profile_image = picture_file

        # Збереження змін у базу даних
        db.session.commit()
        flash('Ваш профіль оновлено!', 'success')
        return redirect(url_for('users.account'))  # Повернення до сторінки профілю

    # Якщо форма недійсна, повертаємо помилки
    flash('Не вдалося оновити профіль. Перевірте дані.', 'danger')
    return redirect(url_for('account'))
from app.users.forms import ChangePasswordForm

@users_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Перевірка поточного пароля
        if not check_password_hash(current_user.password, form.old_password.data):
            flash('Неправильний поточний пароль.', 'danger')
            return redirect(url_for('profile'))
        
        # Перевірка нового пароля та підтвердження
        if form.new_password.data != form.confirm_password.data:
            flash('Новий пароль і підтвердження не збігаються.', 'danger')
            return redirect(url_for('profile'))
        
        # Оновлення пароля користувача
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Ваш пароль успішно змінено!', 'success')
        return redirect(url_for('users.get_profile'))
    
    # Якщо форма недійсна, повертаємо помилки
    flash('Не вдалося змінити пароль. Перевірте введені дані.', 'danger')
    return redirect(url_for('users.get_profile'))








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



@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    from app.users.models import User
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Обробка фото профілю
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)  # Зберігаємо фото
        else:
            picture_file = 'default.jpg'  # Якщо немає фото, використовуємо дефолтне

        # Створення нового користувача
        new_user = User(username=username, email=email, password=hashed_password, image_file=picture_file)  # Використовуємо image_file
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form, title='Register')

import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Зміна розміру зображення
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn
