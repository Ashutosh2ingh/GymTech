from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship(
        'Profile',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

class Plan(db.Model):

    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    features = db.relationship(
        'PlanFeature',
        backref='plan',
        cascade='all, delete-orphan'
    )

class PlanFeature(db.Model):

    __tablename__ = 'plan_features'

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(
        db.Integer,
        db.ForeignKey('plans.id'),
        nullable=False
    )
    feature_name = db.Column(db.String(255), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

class Profile(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    image = db.Column(
        db.String(255),
        default='about.png'
    )
    user_type = db.Column(
        db.Enum('Member', 'Admin', name='user_types'),
        nullable=False,
        default='Member'
    )
    plan_id = db.Column(
        db.Integer,
        db.ForeignKey('plans.id'),
        nullable=True
    )
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    plan = db.relationship('Plan')

class Employee(db.Model):

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    image = db.Column(db.String(255), nullable=True, default="about.png")
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(
        db.Enum("Male", "Female", "Other", name="gender_types"),
        nullable=False
    )
    employee_type = db.Column(
        db.Enum(
            "Manager",
            "Trainer",
            "Receptionist",
            "Helper",
            "Cleaner",
            name="employee_types"
        ),
        nullable=False
    )
    joining_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    trainer = db.relationship(
        "Trainer",
        backref="employee",
        uselist=False,
        cascade="all, delete-orphan"
    )
    salaries = db.relationship(
        "Salary",
        backref="employee",
        cascade="all, delete-orphan"
    )

    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )
    
class Trainer(db.Model):

    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False,
        unique=True
    )
    speciality = db.Column(db.String(255), nullable=False)
    trainer_type = db.Column(
        db.Enum(
            "General Trainer",
            "Personal Trainer",
            name="trainer_types"
        ),
        nullable=False
    )
    pt_monthly_fee = db.Column(
        db.Integer,
        nullable=True
    )

class Salary(db.Model):

    __tablename__ = "salaries"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    credited = db.Column(
        db.Boolean,
        default=False
    )
    credited_on = db.Column(
        db.DateTime,
        nullable=True
    )

class Equipment(db.Model):

    __tablename__ = "equipments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    purpose = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(255),nullable=False,default="about.png")
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )