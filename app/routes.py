from flask import render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from app.models import User, UserActivity
import re
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def log_activity(action, user_id=None):
    activity = UserActivity(user_id=user_id, action=action)
    db.session.add(activity)
    db.session.commit()


@login_manager.unauthorized_handler
def unauthorized():
    if request.endpoint not in ['register', 'home', 'login']:
        flash('Please log in to access this page.', 'error')
    return redirect(url_for('login'))

@app.route('/export/<format>', methods=['GET'])
@login_required
def export_data(format):
    #
    users = User.query.all()
    user_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]

    if format == "json":
        
        log_activity('Exported data as JSON', user_id=current_user.id)
        return Response(
            response=jsonify(user_data).get_data(as_text=True),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=users.json"}
        )

    elif format == "text":
        
        text_data = "\n".join([f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}" for user in user_data])
        log_activity('Exported data as text', user_id=current_user.id)
        return Response(text_data, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=users.txt"})

    else:
        return "Invalid format! Use 'json' or 'text'.", 400

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/search', methods=['GET'])
@login_required
def search_users():
    query = request.args.get('query', '').strip()
    results = []
    if query:
        results = User.query.filter(
            (User.name.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
        ).all()
    log_activity('Search performed', user_id=current_user.id)
    return render_template('index.html', users=results, search_query=query)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        location = request.form.get('location')
        latlong = request.form.get('latlong')

        if not name or not email or not password or not location or not latlong:
            return redirect(url_for('register', error='All fields are required.'))

        # Validate email format
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return redirect(url_for('register', error='Invalid email format.'))

        # Validate latitude and longitude format
        latlong_pattern = r"^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$"
        if not re.match(latlong_pattern, latlong):
            return redirect(url_for('register', error='Invalid latitude, longitude format.'))

        try:
            latitude, longitude = map(float, latlong.split(','))
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                raise ValueError
        except ValueError:
            return redirect(url_for('register', error='Latitude must be between -90 and 90, and longitude between -180 and 180.'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('register', error='Email is already registered. Please log in.'))

        new_user = User(name=name, email=email, location=location, latitude=latitude, longitude=longitude)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        log_activity('User registered', user_id=new_user.id)

        return redirect(url_for('login', success='Registration successful! Please log in.'))

    return render_template('register.html', error=request.args.get('error'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        location = request.form.get('location')
        latlong = request.form.get('latlong')

        if not name or not email or not location or not latlong:
            return redirect(url_for('add_user', error='All fields are required.'))

        latlong_pattern = r"^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$"
        if not re.match(latlong_pattern, latlong):
            return redirect(url_for('add_user', error='Invalid latitude, longitude format.'))

        try:
            latitude, longitude = map(float, latlong.split(','))
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                raise ValueError
        except ValueError:
            return redirect(url_for('add_user', error='Latitude must be between -90 and 90, and longitude between -180 and 180.'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('add_user', error='Email is already registered.'))

        new_user = User(name=name, email=email, location=location, latitude=latitude, longitude=longitude)
        db.session.add(new_user)
        db.session.commit()
        log_activity('User added', user_id=current_user.id)
        return redirect(url_for('index', success='User added successfully!'))

    return render_template('add_user.html', error=request.args.get('error'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        location = request.form.get('location')
        latlong = request.form.get('latlong')

        if not name or not email or not location or not latlong:
            return redirect(url_for('edit_user', id=id, error='All fields are required.'))

        latlong_pattern = r"^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$"
        if not re.match(latlong_pattern, latlong):
            return redirect(url_for('edit_user', id=id, error='Invalid latitude, longitude format.'))

        try:
            latitude, longitude = map(float, latlong.split(','))
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                raise ValueError
        except ValueError:
            return redirect(url_for('edit_user', id=id, error='Latitude must be between -90 and 90, and longitude between -180 and 180.'))

        user.name = name
        user.email = email
        user.location = location
        user.latitude = latitude
        user.longitude = longitude

        db.session.commit()
        log_activity('User edited', user_id=current_user.id)
        return redirect(url_for('index', success='User updated successfully!'))

    return render_template('edit_user.html', user=user, error=request.args.get('error'))

@app.route('/delete/<int:id>')
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    log_activity('User deleted', user_id=current_user.id)
    return redirect(url_for('index', success='User deleted successfully!'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return redirect(url_for('login', error='Both email and password are required.'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            log_activity('User logged in', user_id=user.id)
            return redirect(url_for('index', success='Logged in successfully!'))

        return redirect(url_for('login', error='Invalid email or password.'))

    return render_template('login.html', success=request.args.get('success'), error=request.args.get('error'))

@app.route('/logout')
@login_required
def logout():
    log_activity('User logged out', user_id=current_user.id)
    logout_user()
    return redirect(url_for('login', success='Logged out successfully!'))

