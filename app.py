# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(**name**)
app.config[‘SECRET_KEY’] = ‘your-secret-key-here’
app.config[‘SQLALCHEMY_DATABASE_URI’] = ‘sqlite:///bookportal.db’
app.config[‘SQLALCHEMY_TRACK_MODIFICATIONS’] = False

db = SQLAlchemy(app)

# Модели базы данных

class User(db.Model):
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(80), nullable=False)
email = db.Column(db.String(120), unique=True, nullable=False)
phone = db.Column(db.String(20), nullable=False)
password_hash = db.Column(db.String(128), nullable=False)
is_admin = db.Column(db.Boolean, default=False)
books = db.relationship(‘Book’, backref=‘owner’, lazy=True)

class Book(db.Model):
id = db.Column(db.Integer, primary_key=True)
title = db.Column(db.String(200), nullable=False)
author = db.Column(db.String(100), nullable=False)
description = db.Column(db.Text)
is_available = db.Column(db.Boolean, default=True)
date_added = db.Column(db.DateTime, default=datetime.utcnow)
user_id = db.Column(db.Integer, db.ForeignKey(‘user.id’), nullable=False)

# Создание таблиц

with app.app_context():
db.create_all()

@app.route(’/’)
def index():
books = Book.query.filter_by(is_available=True).all()
return render_template(‘index.html’, books=books)

@app.route(’/register’, methods=[‘GET’, ‘POST’])
def register():
if request.method == ‘POST’:
name = request.form[‘name’]
email = request.form[‘email’]
phone = request.form[‘phone’]
password = request.form[‘password’]

```
    # Проверка на существующего пользователя
    if User.query.filter_by(email=email).first():
        flash('Пользователь с таким email уже существует')
        return render_template('register.html')
    
    # Создание нового пользователя
    user = User(
        name=name,
        email=email,
        phone=phone,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    
    flash('Регистрация успешна!')
    return redirect(url_for('login'))

return render_template('register.html')
```

@app.route(’/login’, methods=[‘GET’, ‘POST’])
def login():
if request.method == ‘POST’:
email = request.form[‘email’]
password = request.form[‘password’]

```
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['is_admin'] = user.is_admin
        flash('Вход успешен!')
        return redirect(url_for('profile'))
    else:
        flash('Неверный email или пароль')

return render_template('login.html')
```

@app.route(’/logout’)
def logout():
session.clear()
flash(‘Вы вышли из системы’)
return redirect(url_for(‘index’))

@app.route(’/profile’)
def profile():
if ‘user_id’ not in session:
return redirect(url_for(‘login’))

```
user = User.query.get(session['user_id'])
user_books = Book.query.filter_by(user_id=session['user_id']).all()
return render_template('profile.html', user=user, books=user_books)
```

@app.route(’/add_book’, methods=[‘GET’, ‘POST’])
def add_book():
if ‘user_id’ not in session:
return redirect(url_for(‘login’))

```
if request.method == 'POST':
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    
    book = Book(
        title=title,
        author=author,
        description=description,
        user_id=session['user_id']
    )
    db.session.add(book)
    db.session.commit()
    
    flash('Книга добавлена!')
    return redirect(url_for('profile'))

return render_template('add_book.html')
```

@app.route(’/admin’)
def admin():
if ‘user_id’ not in session or not session.get(‘is_admin’):
flash(‘Доступ запрещен’)
return redirect(url_for(‘index’))

```
users = User.query.all()
books = Book.query.all()
return render_template('admin.html', users=users, books=books)
```

@app.route(’/delete_book/<int:book_id>’)
def delete_book(book_id):
if ‘user_id’ not in session:
return redirect(url_for(‘login’))

```
book = Book.query.get_or_404(book_id)

# Проверка прав (владелец или админ)
if book.user_id == session['user_id'] or session.get('is_admin'):
    db.session.delete(book)
    db.session.commit()
    flash('Книга удалена')
else:
    flash('Нет прав для удаления')

return redirect(url_for('profile'))
```

if **name** == ‘**main**’:
app.run(debug=True)
