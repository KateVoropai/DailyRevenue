from app import app, db
from models import User, Price, Employees, Calculate, Report
from flask import render_template, redirect, url_for, request, flash, Response
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@app.route('/')
@login_required
def index():
    return render_template('base.html')


@app.route('/price', methods=['GET', 'POST'])
@login_required
def price():
    if request.method == 'GET':
        price = Price.query.all()
        return render_template('price.html', price=price)
    name_service = request.form.get('name_service')
    car = request.form.get('car')
    jeep = request.form.get('jeep')
    minivan = request.form.get('minivan')
    if not car.isdigit() or not jeep.isdigit() or not minivan.isdigit():
        flash({'title': "Статус", 'message': "Поля 'ЛЕГКОВОЙ АВТОМОБИЛЬ', 'ДЖИП', 'МИНИВЕН' должны содержать только цифры!"}, 'error')
        return redirect(url_for('price'))
    price = Price(name_service=name_service, car=car, jeep=jeep, minivan=minivan)
    db.session.add(price)
    db.session.commit()
    price = Price.query.all()
    return render_template('price.html', price=price)

@app.route('/price/update', methods=['POST'])
@login_required
def price_update():
    price_id = int(request.form.get('id'))
    name_service = request.form.get('name_service')
    car = request.form.get('car')
    jeep = request.form.get('jeep')
    minivan = request.form.get('minivan')
    if not car.isdigit() or not jeep.isdigit() or not minivan.isdigit():
        flash({'title': "Статус", 'message': "Поля 'ЛЕГКОВОЙ АВТОМОБИЛЬ', 'ДЖИП', 'МИНИВЕН' должны содержать только цифры!"}, 'error')
        return redirect(url_for('price'))
    
    price_obj = Price.query.get(price_id) 
    price_obj.name_service = name_service
    price_obj.car = car
    price_obj.jeep = jeep
    price_obj.minivan = minivan
    db.session.add(price_obj)
    db.session.commit()
    return redirect(url_for('price'))

@app.route('/price/delete', methods=['POST'])
@login_required
def price_delete():
    price_id = int(request.form.get('id'))
    price_obj = Price.query.get(price_id)
    db.session.delete(price_obj)
    db.session.commit()
    return redirect(url_for('price'))


@app.route('/employees', methods=['GET', 'POST'])
@login_required
def employees():
    if request.method == 'GET':
        employees = Employees.query.all()
        return render_template('employees.html', employees=employees)
    name = request.form.get('name')
    post = request.form.get('post')
    if not name.replace(' ', '').isalpha():
        flash({'title': "Статус", 'message': "Поле 'ФИО' должно содержать только буквы!"}, 'error')
        return redirect(url_for('employees'))
    employees = Employees(name=name, post=post)
    db.session.add(employees)
    db.session.commit()
    employees = Employees.query.all()
    return render_template('employees.html', employees=employees)


@app.route('/employees/update', methods=['POST'])
@login_required
def employees_update():
    employees_id = int(request.form.get('id'))
    employees_name = request.form.get('name')
    employees_post = request.form.get('post')
    if not employees_name.replace(' ', '').isalpha():
        flash({'title': "Статус", 'message': "Поле 'ФИО' должно содержать только буквы!"}, 'error')
        return redirect(url_for('employees'))
    employees_obj = Employees.query.get(employees_id)
    employees_obj.name = employees_name
    employees_obj.post = employees_post
    db.session.add(employees_obj)
    db.session.commit()
    return redirect(url_for('employees'))

@app.route('/employees/delete', methods=['POST'])
@login_required
def employees_delete():
    employees_id = int(request.form.get('id'))
    employees_obj = Employees.query.get(employees_id)
    db.session.delete(employees_obj)
    db.session.commit()
    return redirect(url_for('employees'))


@app.route('/calculate', methods=['GET', 'POST'])
@login_required
def calculate():
    if request.method == 'GET':
        price = Price.query.all()
        calculate = Calculate.query.all()
        return render_template('calculate.html', calculate=calculate, price=price)
    
    name_service = request.form.get('name_service')
    percent = request.form.get('percent')
    if not percent.isdigit():
        flash({'title': "Статус", 'message': "Поле 'З/П, %' должно содержать только цифры!"}, 'error')
        return redirect(url_for('calculate'))
    calculate = Calculate(percent=percent, name_service=name_service)
    db.session.add(calculate)
    db.session.commit()
    calculate = Calculate.query.all()
    return render_template('calculate.html', calculate=calculate)


@app.route('/calculate/update', methods=['POST'])
@login_required
def calculate_update():
    calculate_id = int(request.form.get('id'))
    name_service = request.form.get('name_service')
    percent = request.form.get('percent')
    if not percent.isdigit():
        flash({'title': "Статус", 'message': "Поле 'З/П, %' должно содержать только цифры!"}, 'error')
        return redirect(url_for('calculate'))
    calculate_obj = Calculate.query.get(calculate_id)
    calculate_obj.name_service = name_service
    calculate_obj.percent = percent
    db.session.add(calculate_obj)
    db.session.commit()
    return redirect(url_for('calculate'))


@app.route('/calculate/delete', methods=['POST'])
@login_required
def calculate_delete():
    calculate_id = int(request.form.get('id'))
    calculate_obj = Calculate.query.get(calculate_id)
    db.session.delete(calculate_obj)
    db.session.commit()
    return redirect(url_for('calculate'))

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    date_now = str(datetime.now())[:10].split('-')
    date_now = datetime(year=int(date_now[0]), month=int(date_now[1]), day=int(date_now[2]))
    if request.method == 'GET':
        employees = Employees.query.with_entities(Employees.name).all()
        price = Price.query.with_entities(Price.name_service).all()
        report = Report.query.filter(Report.date == date_now).all()
        total = sum([int(i.amount) for i in report])
        return render_template('report.html', employees=employees, price=price, report=report, total=total)
    
    date = request.form.get('date')
    username = request.form.get('username')
    name_service = request.form.get('name_service')
    amount = request.form.get('amount')
    if not amount.isdigit():
        flash({'title': "Статус", 'message': "Поле 'Стоимость услуги' должно содержать только цифры!"}, 'error')
        return redirect(url_for('report'))
    
    try:
        date = [int(i) for i in date.split('.')]
        date = datetime(date[2], date[1], date[0])
    except ValueError:
        flash({'title': "Статус", 'message': "Введите правильный формат в поле дата!"}, 'error')
        return redirect(url_for('report')) 
    
    calculate = Calculate.query.filter_by(name_service=name_service).first()
    report = Report(date=date, username=username, name_service=name_service, amount=amount, salary=calculate.percent)
    db.session.add(report)
    db.session.commit()
    report = Report.query.filter(Report.date == date_now).all()
    total = sum([int(i.amount) for i in report])
    return render_template('report.html', report=report, total=total)


@app.route('/report/update', methods=['POST'])
@login_required
def report_update():
    report_id = int(request.form.get('id'))
    date = request.form.get('date')
    username = request.form.get('username')
    name_service = request.form.get('name_service')
    amount = request.form.get('amount')
    if not amount.isdigit():
        flash({'title': "Статус", 'message': "Поле 'Стоимость услуги' должно содержать только цифры!"}, 'error')
        return redirect(url_for('report'))
    
    try:
        date = [int(i) for i in date.split('.')]
        date = datetime(date[2], date[1], date[0])
    except ValueError:
        flash({'title': "Статус", 'message': "Введите правильный формат в поле дата!"}, 'error')
        return redirect(url_for('report'))
    
    report_obj = Report.query.get(report_id)
    report_obj.date = date
    report_obj.username = username
    report_obj.name_service = name_service
    report_obj.amount = amount
    db.session.add(report_obj)
    db.session.commit()
    return redirect(url_for('report'))


@app.route('/report/delete', methods=['POST'])
@login_required
def report_delete():
    report_id = int(request.form.get('id'))
    report_obj = Report.query.get(report_id)
    db.session.delete(report_obj)
    db.session.commit()
    return redirect(url_for('report'))

@app.route('/report/display', methods=['POST'])
@login_required
def report_display():
    date = request.form.get('date')   
    try:
        date = [int(i) for i in date.split('.')]
        date = datetime(date[2], date[1], date[0])
    except ValueError:
        flash({'title': "Статус", 'message': "Введите правильный формат в поле дата!"}, 'error')
        return redirect(url_for('report'))      
    report = Report.query.filter(Report.date == date).all()
    total = sum([int(i.amount) for i in report])
    return render_template('report.html', report=report, total=total)


@app.route('/salary', methods=['GET', 'POST'])
@login_required
def salary():
    if request.method == 'GET':
        return render_template('salary.html', date='')
    date = request.form.get('date')
    
    try:
        date = [int(i) for i in date.split('.')]
        date = datetime(date[2], date[1], date[0])
    except ValueError:
        flash({'title': "Статус", 'message': "Введите правильный формат в поле дата!"}, 'error')
        return redirect(url_for('salary'))
    
    salary = Report.query.filter(Report.date == date).with_entities(Report.username, db.func.sum(Report.amount*Report.salary//100)).group_by(Report.username).all()
    total = sum([i[1] for i in salary])
    return render_template('salary.html', salary=salary, date=date, total=total)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    login = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=login).first()
    if user is None or not check_password_hash(user.password, password):
        flash({'title': "Статус", 'message': "Неверные данные!"}, 'error')
        return redirect(url_for('login'))
    login_user(user)
    flash({'title': "Статус", 'message': "Успешная авторизация"}, 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    login = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if not (3 < len(login) < 32 and 3 < len(password) < 32):
        flash({'title': "Статус", 'message': "Логин и пароль должны быть от 3 до 32 символов!"}, 'error')
        return redirect(url_for('register'))
    if not password == password2:
        flash({'title': "Статус", 'message': "Пароли не совпадают!"}, 'error')
        return redirect(url_for('register'))
    
    password = generate_password_hash(password)
    user = User(username=login, password=password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash({'title': "Статус", 'message': "Успешная авторизация"}, 'success')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_sign(response: Response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response


