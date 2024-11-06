from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
import json
import os
from datetime import datetime


#posts = [
#    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
#    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
#    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
#] 
# Шлях до JSON-файлу
POSTS_FILE_PATH = 'app/posts/posts.json'

# Завантаження постів із JSON-файлу
def load_posts():
    if os.path.exists(POSTS_FILE_PATH):
        with open(POSTS_FILE_PATH, 'r') as file:
            return json.load(file)
    return []

# Збереження постів у JSON-файл
def save_posts(posts):
    with open(POSTS_FILE_PATH, 'w') as file:
        json.dump(posts, file, indent=4)

@post_bp.route('/')
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    posts = load_posts()
    # Перевірка, чи існує пост із даним ID
    post = next((post for post in posts if post["id"] == id), None)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    print("Form object:", form)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author = session.get('username', 'Anonymous')  # Отримуємо автора з сесії

        # Завантажуємо існуючі пости з JSON-файлу
        posts = load_posts()

        # Створюємо новий пост
        new_post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content,
            "author": author,
            "category": "General",  # Можна змінити на поле з форми
            "is_active": True,
            "publication_date": datetime.now().strftime('%Y-%m-%d')
        }

        # Додаємо новий пост до списку постів
        posts.append(new_post)
        save_posts(posts)  # Зберігаємо у JSON-файл

        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    print(form)
    return render_template('add_post.html', form=form)



@post_bp.errorhandler(404)
def page_not_found(error):
# Відображаємо шаблон 404.html і повертаємо статусний код 404
    return render_template('404.html'), 404