from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


users = {}

# sample courses available to book
courses = [
    {"id": 1, "title": "Python 101", "slots": 10, "description": "Intro to Python programming."},
    {"id": 2, "title": "Web Development", "slots": 8, "description": "Build web apps with Flask."},
    {"id": 3, "title": "Data Science", "slots": 5, "description": "Basics of data analysis."},
]
# uploads folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
            # validate age if provided
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
    return render_template("dashboard.html", username=username)


@app.route('/courses', methods=['GET', 'POST'])
def courses_page():
    message = ""
    username = request.values.get('username', '')

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        username = request.form.get('username', '')
        mode = request.form.get('mode', 'online')
        gender = request.form.get('gender', '')
        country = request.form.get('country', '')
        file = request.files.get('document')

        if not username or username not in users:
            message = "Invalid user. Please login first."
            return render_template('book_courses.html', username=username, courses=courses, message=message, users=users)

        # validate course id
        try:
            cid = int(course_id)
        except (TypeError, ValueError):
            message = "Invalid course selected."
            return render_template('book_courses.html', username=username, courses=courses, message=message, users=users)

        course = next((c for c in courses if c['id'] == cid), None)
        if not course:
            message = "Course not found."
            return render_template('book_courses.html', username=username, courses=courses, message=message, users=users)

        # handle file upload
        saved_filename = None
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(saved_path)
                # expose via relative path from app root
                saved_filename = os.path.relpath(saved_path).replace('\\', '/')
            else:
                message = "Only PDF files are allowed for upload."
                return render_template('book_courses.html', username=username, courses=courses, message=message, users=users)

        # initialize bookings list
        users[username].setdefault('bookings', [])
        # prevent duplicate booking of same course/mode
        existing = [b for b in users[username]['bookings'] if b.get('course_id') == cid and b.get('mode') == mode]
        if existing:
            message = f"You have already booked '{course['title']}' ({mode})."
        else:
            users[username]['bookings'].append({
                'course_id': cid,
                'mode': mode,
                'gender': gender,
                'country': country,
                'filename': saved_filename,
            })
            message = f"Successfully booked '{course['title']}' ({mode})."

    return render_template('book_courses.html', username=username, courses=courses, message=message, users=users)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

@app.route('/sayHello')   
def hello():
    username = request.args.get('username', 'Guest')
    return f"Hello, {username}!"


if __name__ == "__main__":
    app.run(debug=True)
