from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from base import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
db = Database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def view_login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def view_register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if db.verify_password(email, password):
        session['logged_in'] = True
        session['email'] = email
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if db.get_user(username):
        return jsonify({"message": "Username already exists"}), 400
    if db.get_user_by_email(email):
        return jsonify({"message": "Email already exists"}), 400
    if db.get_user_by_phone(phone):
        return jsonify({"message": "Phone already exists"}), 400

    db.create_user(first_name, last_name, username, email, phone, password=password)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    email = session.get('email')
    user = db.get_user_by_email(email)
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)