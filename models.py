"""
Data Model Classes for Vezeeta Healthcare System
"""


class User:
    """Represents a patient user in the healthcare system"""
    
    def __init__(self, username, age=None):
        self.username = username
        self.password = None
        self.age = age
        self.appointments = []
    
    def set_password(self, password_hash):
        """Set the hashed password"""
        self.password = password_hash
    
    def add_appointment(self, appointment):
        """Add an appointment to user's appointments list"""
        self.appointments.append(appointment)
    
    def get_appointments(self):
        """Get all appointments for this user"""
        return self.appointments
    
    def to_dict(self):
        """Convert user to dictionary for session/template use"""
        return {
            'username': self.username,
            'age': self.age,
            'appointments_count': len(self.appointments)
        }


class Doctor:
    """Represents a doctor in the healthcare system"""
    
    def __init__(self, id, name, specialty, hospital, slots):
        self.id = id
        self.name = name
        self.specialty = specialty
        self.hospital = hospital
        self.slots = slots
    
    def to_dict(self):
        """Convert doctor to dictionary for templates"""
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'hospital': self.hospital,
            'slots': self.slots
        }


class Appointment:
    """Represents a scheduled appointment"""
    
    def __init__(self, doctor_id, doctor_name, specialty, hospital, 
                 appointment_date, appointment_time, phone, symptoms):
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.specialty = specialty
        self.hospital = hospital
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.phone = phone
        self.symptoms = symptoms
    
    def to_dict(self):
        """Convert appointment to dictionary for templates"""
        return {
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor_name,
            'specialty': self.specialty,
            'hospital': self.hospital,
            'appointment_date': self.appointment_date,
            'appointment_time': self.appointment_time,
            'phone': self.phone,
            'symptoms': self.symptoms
        }
