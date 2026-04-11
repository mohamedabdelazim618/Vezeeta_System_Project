class Car:
    def __init__(self, name, model, year):
        self.name = name
        self.model = model
        self.year = year
        
my_car = Car("Xiaomi", "SU7 Ultra", 2025)
your_car = Car("BYD", "seal7", 2024)
print(f"My car is a {my_car.name} {my_car.model} {my_car.year}.")
print(f"Your car is a {your_car.name} {your_car.model} {your_car.year}.")

#encapsulation
class students:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
        
    def get_name(self, name):
        return self.name
    
    def get_age(self, age):
        return self.age
    
    def get_grade(self, grade):
        return self.grade
    
   

student1 = students("Alice", 20, 85)
print(f"Student 1: {student1.get_name('Alice')}, Age: {student1.get_age(20)}, Grade: {student1.get_grade(85)}")

class instructor:
    def __init__(self, name, age, subject):
        self.name = name
        self.age = age
        self.subject = subject
        
    def get_name(self, name):
        return self.name
    
    def get_age(self, age):
        return self.age
    
    def get_subject(self, subject):
        return self.subject 
    
instructor1 = instructor("Bob", 30, "Mathematics")
print(f"Instructor 1: {instructor1.get_name('Bob')}, Age: {instructor1.get_age(30)}, Subject: {instructor1.get_subject('Mathematics')}")

# #inheritance

class vehicle:
    def __init__(self, model):
        self.model = model

class car(vehicle):
    def __init__(self, model, brand):
        super().__init__(model)
        self.brand = brand 
car = car("SU7 Ultra", "Xiaomi")
print(f"Car : {car.brand} {car.model}") 

class train(vehicle):
    def __init__(self, model, route):
        super().__init__(model)
        self.route = route
train = train("Bullet Train", "Tokyo to Osaka")
print(f"Train : {train.model} Route: {train.route}")

#polymorphism

class shape:
    def area(self):
        pass


#abstraction

from abc import ABC, abstractmethod

class CoffeeMachine(ABC):
    @abstractmethod
    def make_coffee(self):
        pass

class EspressoMachine(CoffeeMachine):
    def make_coffee(self):
        return "Making an espresso."
    
class LatteMachine(CoffeeMachine):
    def make_coffee(self):
        return "Making a latte."
    
espresso_machine = EspressoMachine()
latte_machine = LatteMachine()
print(espresso_machine.make_coffee())
print(latte_machine.make_coffee())


    

