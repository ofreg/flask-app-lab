
from flask import render_template
from . import recipes_bp
import os
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
from app import db
from app.recipes.models import Recipe
from app.recipes.forms import RecipeForm
@recipes_bp.route('/')
def main_page():
    """
    Головна сторінка з 15 рецептами страв.
    """
    return render_template('main.html')




@recipes_bp.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('detail_recipe.html', recipe=recipe)






import os
from flask import current_app
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, request, flash
from . import recipes_bp
from .models import Recipe, Category
from .forms import RecipeForm
from app import db
from flask_login import login_required

# Шлях для збереження зображень
import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    # Генерація випадкового імені для файлу
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Вказуємо правильний шлях до збереження файлу
    picture_path = os.path.join(current_app.root_path, 'recipes', 'static', 'uploads', picture_fn)

    # Перевірка на існування папки, якщо її немає, то створюємо
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Зміна розміру зображення на 250x250 пікселів
    output_size = (250, 250)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    # Повертаємо відносний шлях до зображення для збереження в базі даних
    return 'uploads/' + picture_fn



@recipes_bp.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # Перевірка, чи користувач є автором рецепта
    if recipe.user_id != current_user.id:
        flash('Ви не маєте доступу до редагування цього рецепту.', 'danger')
        return redirect(url_for('recipes.recipe_account'))

    categories = Category.query.all()  # Отримуємо всі категорії для випадаючого списку
    form = RecipeForm(obj=recipe)  # Якщо ви використовуєте FlaskForm для заповнення форми

    if form.validate_on_submit():
        # Оновлюємо інформацію про рецепт
        recipe.name = form.name.data
        recipe.category_id = form.category_id.data  # Оновлюємо категорію
        recipe.description = form.description.data
        recipe.cooking_time = form.cooking_time.data
        recipe.ingredients = form.ingredients.data

        # Оновлюємо зображення, якщо воно було завантажене
        if form.image.data:
            # Обробка завантаження зображення
            recipe.image_path = save_picture(form.image.data)  # функція для збереження зображення

        db.session.commit()
        flash('Рецепт успішно оновлено!', 'success')
        return redirect(url_for('recipes.recipe_detail', recipe_id=recipe.id))  # Переходимо на сторінку рецепту після редагування

    return render_template('recipe_edit.html', form=form, recipe=recipe, categories=categories)

@recipes_bp.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    categories = Category.query.all()  # Отримуємо всі категорії з БД

    if form.validate_on_submit():
        image_file = form.image.data
        image_filename = None

        # Обробка зображення
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Додавання нового рецепту
        recipe = Recipe(
            name=form.name.data,
            description=form.description.data,
            cooking_time=form.cooking_time.data,
            ingredients=form.ingredients.data,
            category_id=form.category_id.data,
            image_path=image_filename,
            user_id=current_user.id  # Прив'язка до автора
        )

        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipes.add_recipe'))

    return render_template('add_recipe.html', form=form, categories=categories)



#######################################################################################

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from . import recipes_bp
from .models import RecipeUser
from .forms import RegistrationForm, LoginForm
from app import db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user

from .forms import RegistrationForm
from .models import RecipeUser

# Реєстрація нового користувача
@recipes_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Створюємо користувача
        user = RecipeUser(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Якщо файл завантажено, збережемо його
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
                user.photo = filename  # Додаємо поле для фото до користувача

        db.session.add(user)
        db.session.commit()
        flash('Ви успішно зареєструвались!', 'success')
        login_user(user)
        return redirect(url_for('recipes.main_page'))

    return render_template('recipe_register.html', form=form)

# Вхід користувача
@recipes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = RecipeUser.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('recipes.main_page'))  # Перенаправлення на головну сторінку
        else:
            flash('Невірний емейл або пароль!', 'danger')
    return render_template('recipe_login.html', form=form)

# Вихід користувача
@recipes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('recipes.index'))  # Перенаправлення на головну





@recipes_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    return "Форма скидання пароля"




from flask_login import current_user, login_required
from flask import render_template

from flask import render_template
from flask_login import login_required, current_user

@recipes_bp.route('/recipe_account', methods=['GET'])
@login_required
def recipe_account():
    # Отримуємо користувача та його рецепти
    user = RecipeUser.query.get_or_404(current_user.id)
    recipes = Recipe.query.filter_by(user_id=user.id).all()

    return render_template('recipe_account.html', user=user, recipes=recipes)


###################################################################################################



from sqlalchemy.orm import joinedload
@recipes_bp.route('/recipes', methods=['GET', 'POST'])
def recipes_list():
    form = RecipeForm()

    # Завантажуємо категорії в поле `SelectField`
    form.category_id.choices = [(category.id, category.category_name) for category in Category.query.all()]

    # Отримуємо параметри запиту для сортування та фільтрації
    category_id = request.args.get('category_id')
    sort_field = request.args.get('sort', 'name')  # Значення за замовчуванням - сортування за назвою

    # Фільтрація рецептів за категорією (якщо обрана категорія)
    query = Recipe.query.options(joinedload(Recipe.category))
    if category_id:
        query = query.filter(Recipe.category_id == category_id)

    # Сортування рецептів за вибраним полем
    if sort_field:
        query = query.order_by(getattr(Recipe, sort_field))

    # Отримуємо відфільтровані та відсортовані рецепти
    all_recipes = query.all()

    # Повертаємо шаблон з рецептами
    return render_template('all_recipes.html', form=form, recipes=all_recipes, sort_field=sort_field)




from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from .models import Recipe
from . import recipes_bp

@recipes_bp.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    
    recipe = Recipe.query.get_or_404(recipe_id)
    
    
    if recipe.user_id != current_user.id:
        flash('У вас немає прав на видалення цього рецепта.', 'danger')
        return redirect(url_for('recipes.recipe_account'))
    
    # Видалити рецепт
    try:
        db.session.delete(recipe)
        db.session.commit()
        flash('Рецепт успішно видалено!', 'success')
    except:
        db.session.rollback()
        flash('Виникла помилка при видаленні рецепта.', 'danger')
    
    return redirect(url_for('recipes.recipe_account'))









