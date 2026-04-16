"""
Manager/Repository Classes for Data Management
"""

from models import User, Doctor, Appointment


class UserManager:
    """Manages user registration, retrieval, and authentication data"""
    
    def __init__(self):
        self.users = {}
    
    def register(self, username, password_hash, age=None):
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        if username in self.users:
            return False, "Username already exists"
        
        user = User(username, age)
        user.set_password(password_hash)
        self.users[username] = user
        return True, "Registration successful"
    
    def get_user(self, username):
        """Get user by username, returns User object or None"""
        return self.users.get(username)
    
    def user_exists(self, username):
        """Check if user exists"""
        return username in self.users
    
    def add_appointment_to_user(self, username, appointment):
        """Add an appointment to a user"""
        if username in self.users:
            self.users[username].add_appointment(appointment)
            return True
        return False
    
    def get_user_appointments(self, username):
        """Get all appointments for a user"""
        user = self.get_user(username)
        if user:
            return user.get_appointments()
        return []
    
    def get_all_users(self):
        """Get all users (for admin purposes)"""
        return self.users
    
    def convert_users_to_dict(self):
        """Convert all users to dictionary format for templates"""
        result = {}
        for username, user in self.users.items():
            result[username] = {
                'password': user.password,
                'age': user.age,
                'appointments': [apt.to_dict() for apt in user.appointments]
            }
        return result


class DoctorManager:
    """Manages doctor data"""
    
    def __init__(self):
        self.doctors = {}
        self._initialize_doctors()
    
    def _initialize_doctors(self):
        """Initialize default doctors"""
        doctors_data = [
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
        
        for doc_data in doctors_data:
            doctor = Doctor(
                doc_data["id"],
                doc_data["name"],
                doc_data["specialty"],
                doc_data["hospital"],
                doc_data["slots"]
            )
            self.doctors[doctor.id] = doctor
    
    def get_all(self):
        """Get all doctors as list"""
        return list(self.doctors.values())
    
    def get_by_id(self, doctor_id):
        """Get doctor by ID"""
        return self.doctors.get(doctor_id)
    
    def get_all_as_dict(self):
        """Get all doctors as dictionaries for templates"""
        return [doc.to_dict() for doc in self.doctors.values()]
    
    def add_doctor(self, doctor):
        """Add a new doctor"""
        self.doctors[doctor.id] = doctor
    
    def update_slots(self, doctor_id, new_slots):
        """Update available slots for a doctor"""
        if doctor_id in self.doctors:
            self.doctors[doctor_id].slots = new_slots
            return True
        return False
