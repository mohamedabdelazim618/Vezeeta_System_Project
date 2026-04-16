from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os

# Import OOP classes
from managers import UserManager, DoctorManager
from services import AuthService, AppointmentService

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'

# Initialize managers
user_manager = UserManager()
doctor_manager = DoctorManager()

# Initialize services
auth_service = AuthService(user_manager)
appointment_service = AppointmentService(user_manager, doctor_manager)


@app.route('/')
def home():
    return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        user = request.form.get('username', '').strip()
        pwd = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        age = request.form.get('age', '')

        success, message = auth_service.register(user, pwd, confirm, age)
        if success:
            return redirect(url_for('login'))
    
    return render_template("register.html", message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        user = request.form.get('username', '')
        pwd = request.form.get('password', '')
        
        success, user_obj = auth_service.login(user, pwd)
        if success:
            return redirect(url_for('dashboard', username=user))
        else:
            message = "Invalid username or password!"
    
    return render_template("login.html", message=message)


@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'User')
    doctors = doctor_manager.get_all_as_dict()
    users_dict = user_manager.convert_users_to_dict()
    
    return render_template(
        "dashboard.html", 
        username=username, 
        doctors=doctors, 
        users=users_dict
    )


@app.route('/appointments', methods=['GET', 'POST'])
def appointments_page():
    message = ""
    username = request.values.get('username', '')
    doctors = doctor_manager.get_all_as_dict()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        username = request.form.get('username', '')
        appointment_date = request.form.get('appointment_date', '')
        appointment_time = request.form.get('appointment_time', '')
        phone = request.form.get('phone', '')
        symptoms = request.form.get('symptoms', '')

        success, message = appointment_service.book_appointment(
            username, 
            doctor_id, 
            appointment_date, 
            appointment_time, 
            phone, 
            symptoms
        )

    users_dict = user_manager.convert_users_to_dict()
    return render_template(
        'book_appointments.html', 
        username=username, 
        doctors=doctors, 
        message=message, 
        users=users_dict
    )


@app.route('/doctors')
def doctors_list():
    username = request.args.get('username', 'User')
    doctors = doctor_manager.get_all_as_dict()
    
    return render_template(
        'doctors_list.html', 
        username=username, 
        doctors=doctors
    )


@app.route('/logout')
def logout():
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])