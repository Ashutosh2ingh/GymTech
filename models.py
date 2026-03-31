from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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