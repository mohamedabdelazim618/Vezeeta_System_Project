# Vezeeta System Project

A Flask-based medical appointment booking web application inspired by Vezeeta. It allows patients to register, browse doctors across multiple specialties and hospitals, book appointments, and manage their bookings — all through a clean web interface.

---

## Features

- **User Registration & Login** — Secure account creation with password hashing via Werkzeug.
- **Doctor Directory** — Browse 10 doctors across specialties (Cardiology, Neurology, Dermatology, Pediatrics, and more) and multiple hospitals.
- **Appointment Booking** — Select a doctor, choose a date and time, and provide contact details and symptoms.
- **Duplicate Prevention** — The system prevents double-booking the same doctor at the same date and time slot.
- **Appointment Cancellation** — Cancel any existing booking directly from the appointments page.
- **Patient Dashboard** — View your profile, registered users, and available doctors at a glance.

---

## Project Structure

```
vezeeta_system_project/
├── app.py                  # Main Flask application — routes and business logic
├── models.py               # Data models: User, Doctor, Appointment
├── oop1.py                 # OOP practice module (not used by the app)
├── requirements.txt        # Python dependencies
├── static/
│   ├── app.css
│   ├── dashboard.css
│   ├── doctors_list.css
│   ├── book_appointments.css
│   ├── login.css
│   ├── register.css
│   ├── ui.css
│   └── ui.js
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── doctors_list.html
│   └── book_appointments.html
└── uploads/                # Reserved for future file uploads
```

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3, Flask 3.1.2             |
| Templating | Jinja2 3.1.6                      |
| Security   | Werkzeug password hashing         |
| Config     | python-dotenv                     |
| Server     | Gunicorn (production)             |
| Frontend   | HTML5, CSS3, Vanilla JavaScript   |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone or extract the project:**
   ```bash
   git clone <repository-url>
   cd vezeeta_system_project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Run the development server:**
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`.

### Production Deployment

Use Gunicorn (included in requirements):
```bash
gunicorn -w 4 app:app
```

---

## Usage

1. **Register** a new account at `/register`.
2. **Log in** at `/login` with your credentials.
3. From the **Dashboard**, navigate to the doctor list or appointments page.
4. **Book an appointment** by selecting a doctor, date, time, and entering your phone number and symptoms.
5. **Cancel appointments** from the appointments page when needed.
6. **Log out** to return to the login page.

---

## Data Models

### `User`
Stores username, hashed password, age, and a list of appointments.

### `Doctor`
Stores doctor ID, name, specialty, hospital affiliation, and available slots.

### `Appointment`
Stores the linked doctor, date, time, patient phone number, and reported symptoms.

---

## Current Limitations

- **In-memory storage only** — all data (users and appointments) is lost when the server restarts. A database (e.g. SQLite or PostgreSQL with SQLAlchemy) would be needed for persistence.
- **No session management** — the logged-in username is passed as a URL query parameter rather than via a secure server-side session.
- **No authentication middleware** — routes are not protected; any user can access any page by constructing the right URL.

---

## Dependencies

```
Flask==3.1.2
Werkzeug==3.1.4
Jinja2==3.1.6
python-dotenv==1.0.0
gunicorn==25.1.0
itsdangerous==2.2.0
blinker==1.9.0
click==8.3.1
colorama==0.4.6
MarkupSafe==3.0.3
packaging==26.0
```

---

## License

This project was created for educational purposes.
