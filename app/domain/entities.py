import json

from flask import send_from_directory

from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5


class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    address = db.Column(db.String(256), index=True)
    postalcode = db.Column(db.String(256), index=True)
    city = db.Column(db.String(256), index=True)
    state = db.Column(db.String(256), index=True)
    passport_id = db.Column(db.String(16), index=True, unique=True)
    birth_date = db.Column(db.String(128), index=True)
    marital_status = db.Column(db.String(16), index=True)
    gender = db.Column(db.String(8), index=True)
    occupation = db.Column(db.String(256), index=True)
    invite_code = db.relationship('InviteCode', backref='patient')
    password_hash = db.Column(db.String(256), index=True, unique=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    transfer = db.Column(db.Integer, index=True)
    profile_picture = db.Column(db.String(256))
    consultations = db.relationship('Consultation', backref='patient')
    information_sheet = db.relationship('InformationSheet', backref='patient')
    given_rating = db.Column(db.Integer, index=True)

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None,
                 city=None, state=None, postalcode=None, passport_id=None,
                 birth_date=None, marital_status=None, gender=None, occupation=None, invite_code=None,
                 doctor_id=None, password_hash=None, given_rating=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.postalcode = postalcode
        self.passport_id = passport_id
        self.birth_date = birth_date
        self.marital_status = marital_status
        self.gender = gender
        self.occupation = occupation
        self.password_hash = password_hash
        self.doctor_id = doctor_id
        self.given_rating = given_rating

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return f'Patient: {self.username}'

    def __str__(self):
        return f'Patient: {self.username}'


class Doctor(db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    address = db.Column(db.String(256), index=True)
    postalcode = db.Column(db.String(256), index=True)
    city = db.Column(db.String(256), index=True)
    state = db.Column(db.String(256), index=True)
    birth_date = db.Column(db.String(128), index=True)
    gender = db.Column(db.String(8), index=True)
    consultation_schedule_office = db.Column(db.String(128), index=True)
    consultation_schedule_away = db.Column(db.String(128), index=True)
    assistants_schedule = db.Column(db.String(128), index=True)
    password_hash = db.Column(db.String(256), index=True)
    medical_proof = db.Column(db.String(256))
    profile_picture = db.Column(db.String(256))
    patients = db.relationship('Patient', backref='doctor')
    consultations = db.relationship('Consultation', backref='doctor')

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None,
                 city=None, state=None, postalcode=None,
                 birth_date=None,
                 gender=None, consultation_schedule_office=None, consultation_schedule_away=None,
                 assistants_schedule=None, password_hash=None, rating=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.postalcode = postalcode
        self.birth_date = birth_date
        self.gender = gender
        self.consultation_schedule_office = consultation_schedule_office
        self.consultation_schedule_away = consultation_schedule_away
        self.assistants_schedule = assistants_schedule
        self.password_hash = password_hash
        self.rating = rating

    @property
    def average_rating(self):
        patients = self.patients
        ratings = [patient.given_rating for patient in patients if patient.given_rating is not None]
        if ratings:
            return round(sum(ratings) / len(ratings), 2)
        else:
            return "No rating given"

    @property
    def number_of_patients(self):
        return len(self.patients)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return f'doctor: {self.username}'

    def __str__(self):
        return f'doctor: {self.username}'


class Consultation(db.Model):
    __tablename__ = "consultation"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), )
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date_time = db.Column(db.DateTime, index=True)
    pdf = db.Column(db.String(128))
    urgency_grade = db.Column(db.String(128), index=True)

    def __init__(self, patient_id=None, doctor_id=None, time=None, pdf=None, urgency_grade=None):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = time
        self.pdf = pdf
        self.urgency_grade = urgency_grade


information_sheet_chronic_disease = db.Table('information_sheet_chronic_disease',
                                             db.Column('patient_id', db.Integer,
                                                       db.ForeignKey('information_sheet.patient_id')),
                                             db.Column('chronic_disease_id', db.Integer,
                                                       db.ForeignKey('chronic_disease.id'))
                                             )

information_sheet_allergy = db.Table('information_sheet_allergy',
                                     db.Column('patient_id', db.Integer, db.ForeignKey('information_sheet.patient_id')),
                                     db.Column('allergy_id', db.Integer, db.ForeignKey('allergy.id'))
                                     )


class InformationSheet(db.Model):
    __tablename__ = "information_sheet"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    weight = db.Column(db.Integer, index=True)
    height = db.Column(db.Integer, index=True)
    shoe_size = db.Column(db.Integer, index=True)
    blood_type = db.Column(db.String(256), index=True)
    smoking = db.Column(db.Integer, index=True)
    drinking = db.Column(db.Integer, index=True)
    medical_history = db.relationship('ChronicDisease', secondary=information_sheet_chronic_disease, backref='patients')
    medications = db.relationship('Drug', backref='patient')
    allergies = db.relationship('Allergy', secondary=information_sheet_allergy, backref='patients')

    def init(self, patient_id=None, weigth=None, height=None, shoe_size=None, blood_type=None, smoking=None,
             drinking=None):
        self.patient_id = patient_id
        self.weight = weigth
        self.height = height
        self.shoe_size = shoe_size
        self.blood_type = blood_type
        self.smoking = smoking
        self.drinking = drinking

    @property
    def get_smoking(self):
        if self.smoking == 1:
            return "Yes"
        return "No"

    @property
    def get_drinking(self):
        if self.drinking == 1:
            return "Yes"
        return "No"

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'weight': self.weight,
            'height': self.height,
            'shoe_size': self.shoe_size,
            'blood_type': self.blood_type,
            'smoking': self.get_smoking,
            'drinking': self.get_drinking,
            'medical_history': [disease.name for disease in self.medical_history],
            'medications': [medication.name for medication in self.medications],
            'allergies': [allergy.name for allergy in self.allergies]
        }


class ChronicDisease(db.Model):
    __tablename__ = "chronic_disease"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Drug(db.Model):
    __tablename__ = "drug"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)
    name = db.Column(db.String(256), index=True)
    dosage = db.Column(db.String(256))
    frequency = db.Column(db.String(256))

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Allergy(db.Model):
    __tablename__ = "allergy"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Hospitalization(db.Model):
    __tablename__ = "hospitalization"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'))
    date = db.Column(db.Date)
    reason = db.Column(db.String(500))

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class InviteCode(db.Model):
    __tablename__ = "invite_code"
    id = db.Column(db.Integer, index=True, primary_key=True)
    invite_code = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), index=True)

    def __init__(self, invite_code=None, patient_id=None, doctor_id=None):
        self.invite_code = invite_code
        self.patient_id = patient_id
        self.doctor_id = doctor_id

    def __str__(self):
        return f'{self.invite_code}'

    def __repr__(self):
        return f'{self.invite_code}'
