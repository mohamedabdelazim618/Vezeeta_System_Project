from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'

users = {}

doctors = [
    {"id": 1, "name": "Dr. Ahmed Hassan", "specialty": "General Practitioner", "slots": 10, "hospital": "Cairo Medical Center"},
    {"id": 2, "name": "Dr. Fatima Mohamed", "specialty": "Cardiologist", "slots": 8, "hospital": "Nile Valley Hospital"},
    {"id": 3, "name": "Dr. Omar Khalil", "specialty": "Orthopedist", "slots": 5, "hospital": "Modern Medical Institute"},
    {"id": 4, "name": "Dr. Layla Samir", "specialty": "Dermatologist", "slots": 6, "hospital": "Cairo Medical Center"},
    {"id": 5, "name": "Dr. Hassan Musa", "specialty": "Neurologist", "slots": 4, "hospital": "Nile Valley Hospital"},
    {"id": 6, "name": "Dr. Mona Karim", "specialty": "Pediatrician", "slots": 12, "hospital": "Advanced Medical Center"},
    {"id": 7, "name": "Dr. Youssef Adel", "specialty": "Ophthalmologist", "slots": 7, "hospital": "Modern Medical Institute"},
    {"id": 8, "name": "Dr. Yasmin Helmy", "specialty": "Gynecologist", "slots": 9, "hospital": "Advanced Medical Center"},
    {"id": 9, "name": "Dr. Tarek Saleh", "specialty": "Dentist", "slots": 11, "hospital": "Elite Dental Clinic"},
    {"id": 10, "name": "Dr. Sara Mansour", "specialty": "Psychiatrist", "slots": 5, "hospital": "Mental Health Institute"},
]


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

        if not user or not pwd or not confirm:
            message = "Username, password and confirm password are required"
        elif pwd != confirm:
            message = "Passwords do not match"
        elif user in users:
            message = "Username already exists"
        else:
            age_int = None
            if age:
                try:
                    age_int = int(age)
                    if age_int < 0:
                        raise ValueError()
                except ValueError:
                    message = "Please enter a valid non-negative age"
                    return render_template("register.html", message=message)

            hashed = generate_password_hash(pwd)
            users[user] = {"password": hashed, "age": age_int}
            message = "Registration successful. You can now login."
            return redirect(url_for('login'))
    
    return render_template("register.html", message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        user = request.form.get('username', '')
        pwd = request.form.get('password', '')
       
        if user in users and check_password_hash(users[user]["password"], pwd):
            return redirect(url_for('dashboard', username=user))
        else:
            message = "Invalid username or password!"
    return render_template("login.html", message=message)


@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'User')  
    return render_template("dashboard.html", username=username, doctors=doctors, users=users)


@app.route('/appointments', methods=['GET', 'POST'])
def appointments_page():
    message = ""
    username = request.values.get('username', '')

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        username = request.form.get('username', '')
        appointment_date = request.form.get('appointment_date', '')
        appointment_time = request.form.get('appointment_time', '')
        phone = request.form.get('phone', '')
        symptoms = request.form.get('symptoms', '')

        if not username or username not in users:
            message = "Invalid user. Please login first."
            return render_template('book_appointments.html', username=username, doctors=doctors, message=message, users=users)

        try:
            did = int(doctor_id)
        except (TypeError, ValueError):
            message = "Invalid doctor selected."
            return render_template('book_appointments.html', username=username, doctors=doctors, message=message, users=users)

        doctor = next((d for d in doctors if d['id'] == did), None)
        if not doctor:
            message = "Doctor not found."
            return render_template('book_appointments.html', username=username, doctors=doctors, message=message, users=users)

        if not appointment_date or not appointment_time:
            message = "Please select both date and time for your appointment."
            return render_template('book_appointments.html', username=username, doctors=doctors, message=message, users=users)

        users[username].setdefault('appointments', [])
        existing = [a for a in users[username]['appointments'] if a.get('doctor_id') == did and a.get('appointment_date') == appointment_date and a.get('appointment_time') == appointment_time]
        if existing:
            message = f"You have already booked an appointment with {doctor['name']} at {appointment_time} on {appointment_date}."
        else:
            users[username]['appointments'].append({
                'doctor_id': did,
                'doctor_name': doctor['name'],
                'specialty': doctor['specialty'],
                'hospital': doctor['hospital'],
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'phone': phone,
                'symptoms': symptoms,
            })
            message = f"Appointment successfully booked with {doctor['name']} ({doctor['specialty']}) on {appointment_date} at {appointment_time}."

    return render_template('book_appointments.html', username=username, doctors=doctors, message=message, users=users)


@app.route('/cancel-appointment', methods=['POST'])
def cancel_appointment():
    username = request.form.get('username', '')
    doctor_id = request.form.get('doctor_id', '')
    appointment_date = request.form.get('appointment_date', '')
    appointment_time = request.form.get('appointment_time', '')
    
    message = ""
    
    if not username or username not in users:
        message = "Invalid user. Please login first."
    else:
        try:
            did = int(doctor_id)
        except (TypeError, ValueError):
            message = "Invalid doctor ID."
        
        if did and not message:
            appointments = users[username].get('appointments', [])
            appointment_found = False
            
            for i, apt in enumerate(appointments):
                if (apt.get('doctor_id') == did and 
                    apt.get('appointment_date') == appointment_date and 
                    apt.get('appointment_time') == appointment_time):
                    removed_apt = appointments.pop(i)
                    message = f"Appointment with {removed_apt['doctor_name']} on {appointment_date} at {appointment_time} has been cancelled."
                    appointment_found = True
                    break
            
            if not appointment_found:
                message = "Appointment not found."
    
    return render_template('book_appointments.html', username=username, doctors=doctors, message=message, users=users)


@app.route('/doctors')
def doctors_list():
    username = request.args.get('username', 'User')
    return render_template('doctors_list.html', username=username, doctors=doctors)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])