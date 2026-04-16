"""
Service Classes - Business Logic Layer
"""

from werkzeug.security import generate_password_hash, check_password_hash
from models import Appointment


class AuthService:
    """Handles authentication operations"""
    
    def __init__(self, user_manager):
        self.user_manager = user_manager
    
    def register(self, username, password, confirm_password, age=None):
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        # Validation
        if not username or not password or not confirm_password:
            return False, "Username, password and confirm password are required"
        
        if password != confirm_password:
            return False, "Passwords do not match"
        
        # Validate age if provided
        age_int = None
        if age:
            try:
                age_int = int(age)
                if age_int < 0:
                    raise ValueError()
            except ValueError:
                return False, "Please enter a valid non-negative age"
        
        # Register user
        password_hash = generate_password_hash(password)
        return self.user_manager.register(username, password_hash, age_int)
    
    def login(self, username, password):
        """
        Authenticate user
        Returns: (success: bool, user: User or None)
        """
        user = self.user_manager.get_user(username)
        
        if user and check_password_hash(user.password, password):
            return True, user
        
        return False, None


class AppointmentService:
    """Handles appointment booking and validation"""
    
    def __init__(self, user_manager, doctor_manager):
        self.user_manager = user_manager
        self.doctor_manager = doctor_manager
    
    def book_appointment(self, username, doctor_id, appointment_date, 
                         appointment_time, phone, symptoms):
        
        
        # Validate user
        if not username or not self.user_manager.user_exists(username):
            return False, "Invalid user. Please login first."
        
        user = self.user_manager.get_user(username)
        
        # Validate doctor
        try:
            doctor_id = int(doctor_id)
        except (TypeError, ValueError):
            return False, "Invalid doctor selected."
        
        doctor = self.doctor_manager.get_by_id(doctor_id)
        if not doctor:
            return False, "Doctor not found."
        
        # Validate date and time
        if not appointment_date or not appointment_time:
            return False, "Please select both date and time for your appointment."
        
        # Check for duplicate appointment
        appointments = user.get_appointments()
        for apt in appointments:
            if (apt.doctor_id == doctor_id and 
                apt.appointment_date == appointment_date and 
                apt.appointment_time == appointment_time):
                return False, f"You have already booked an appointment with {doctor.name} at {appointment_time} on {appointment_date}."
        
        # Create and add appointment
        appointment = Appointment(
            doctor_id=doctor_id,
            doctor_name=doctor.name,
            specialty=doctor.specialty,
            hospital=doctor.hospital,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            phone=phone,
            symptoms=symptoms
        )
        
        user.add_appointment(appointment)
        return True, f"Appointment successfully booked with {doctor.name} ({doctor.specialty}) on {appointment_date} at {appointment_time}."
    
    def get_user_appointments(self, username):
        """Get all appointments for a user"""
        appointments = self.user_manager.get_user_appointments(username)
        return [apt.to_dict() for apt in appointments]
