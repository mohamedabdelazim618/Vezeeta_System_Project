class User:
    
    def __init__(self, username, age=None):
        self.username = username
        self.password = None
        self.age = age
        self.appointments = []
    
    def set_password(self, password_hash):
        self.password = password_hash
    
    def add_appointment(self, appointment):
        self.appointments.append(appointment)
    
    def get_appointments(self):
        return self.appointments
    
    def to_dict(self):
        return {
            'username': self.username,
            'age': self.age,
            'appointments_count': len(self.appointments)
        }


class Doctor:
    
    def __init__(self, id, name, specialty, hospital, slots):
        self.id = id
        self.name = name
        self.specialty = specialty
        self.hospital = hospital
        self.slots = slots
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'hospital': self.hospital,
            'slots': self.slots
        }


class Appointment:
    
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
