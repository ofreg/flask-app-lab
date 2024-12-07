import pytest
from flask import Flask

@pytest.fixture
def client():
    # tests/test_user.py


    from app import create_app  # Імпортуємо вашу функцію для створення застосунку
    app = create_app()  # Створюємо застосунок
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Вимикаємо CSRF для тестів
    with app.test_client() as client:
        yield client

def test_register_page(client):
    """Перевірка завантаження сторінки реєстрації"""
    response = client.get('users/register')  # Замініть `/register` на ваш маршрут
    assert response.status_code == 200
    assert b"Register" in response.data  # Перевіряємо наявність тексту на сторінці

def test_login_page(client):
    """Перевірка завантаження сторінки входу"""
    response = client.get('users/login')  # Замініть `/login` на ваш маршрут
    assert response.status_code == 200
    assert b"Login" in response.data  # Перевіряємо наявність тексту на сторінці
