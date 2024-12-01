import json
import os

import flask

from app import app, db
from flask import render_template, redirect, url_for, request, session, send_from_directory, send_file, flash
from app.repository.database import Database
from app.service.service import Service
from twilio.rest import Client
from werkzeug.security import check_password_hash
from werkzeug.exceptions import BadRequest
import datetime

with app.app_context():
    db_1 = Database(db)
    """db_1.clear_chronic_disease_table()
    db_1.clear_allergy_table()
    db_1.clear_patients_table()
    db_1.clear_consultation_table()
    db_1.clear_doctors_table()
    db_1.clear_hospitalization_table()
    db_1.clear_information_sheet_table()
    db_1.clear_invite_code_table()
    db_1.clear_table_1()
    db_1.clear_table_2()"""
    service = Service(db_1, session, choice=False)


class Routes:

    def __init__(self):
        self.__run_all_routes()

    def __run_all_routes(self):
        self.home()
        self.choice()
        self.medic_profile()
        self.transfer_patients()
        self.patient_list()
        self.invite_patient()
        self.medic_home()
        self.register_patient()
        self.register_medic()
        self.register_page_patient()
        self.register_page_medic()
        self.login()

    @staticmethod
    @app.before_request
    def before_request():
        flask.session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=5)
        flask.session.modified = True

    @staticmethod
    @app.route('/clear-session', methods=['GET'])
    def clear_session():
        session.clear()
        return 'Session Cleared'

    @staticmethod
    @app.route('/')
    @app.route('/home')
    def home():
        if "doctor" in service.session:
            return redirect(url_for('medic_home'))
        elif "patient" in service.session:
            return redirect(url_for('patient_home'))
        return render_template('index.html')

    @staticmethod
    @app.route('/register-medic')
    def register_page_medic():
        return render_template('register_medic.html')

    @staticmethod
    @app.route('/register-patient')
    def register_page_patient():
        return render_template('register_patient.html')

    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if "doctor" in service.session:
            return redirect(url_for('medic_home'))
        elif "patient" in service.session:
            return redirect(url_for('patient_home'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            doctor = service.get_doctor_by_username(str(username))
            patient = service.get_patient_by_username(str(username))
            if doctor is not None:
                if check_password_hash(doctor.password_hash, password):
                    service.session['doctor'] = doctor.id
                    return redirect(url_for('medic_home'))
                else:
                    error = 'Wrong password. Try again.'
            elif patient is not None:
                if not check_password_hash(patient.password_hash, password):
                    service.session['patient'] = patient.id
                    return redirect(url_for('patient_home'))
                else:
                    error = 'Wrong password. Try again.'
            else:
                error = 'The username does not exist. Try again.'
        return render_template('login.html', error=error)

    @staticmethod
    @app.route('/logout')
    def logout():
        if 'doctor' in service.session:
            service.session.pop('doctor', None)
        else:
            service.session.pop('patient', None)
        return redirect(url_for('home'))

    @staticmethod
    @app.route('/register-medic', methods=['GET', 'POST'])
    def register_medic():
        error = None
        if request.method == 'POST':
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'],
                         request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password'], request.form['gender'],
                         request.form['zipcode'], request.form['city'],
                         request.form['county'],
                         request.files['profile_picture'], request.files['proof_of_medic']]
            try:
                service.register_medic(form_data)
            except ValueError as exception:
                error = exception
            except AttributeError as exception:
                error = exception
            else:
                service.update_database()
                return redirect(url_for('home'))
        return render_template('register_medic.html', error=error)

    @staticmethod
    @app.route('/register-patient', methods=['GET', 'POST'])
    def register_patient():
        error = None
        if request.method == 'POST':
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['zipcode'], request.form['city'],
                         request.form['county'], request.form['passport_id'],
                         request.form['birth_date'], request.form['marital_status'],
                         request.form['gender'], request.form['occupation'], request.form['password'],
                         request.files['profile_picture'], request.form['invite_code']]
            try:
                service.register_patient(form_data)
            except ValueError as exception:
                error = exception
            else:
                return redirect(url_for('register_patient_2'))
        return render_template('register_patient.html', error=error)

    @staticmethod
    @app.route('/register-patient-2', methods=['GET', 'POST'])
    def register_patient_2():
        error = None
        diseases = [{'name': 'AIDS/HIV', 'type': ''}, {'name': 'Anemia', 'type': ''}, {'name': 'Anxiety', 'type': ''},
                    {'name': 'Arthritis', 'type': 'Type'},
                    {'name': 'Artificial Heart Valve', 'type': ''}, {'name': 'Artificial Joint', 'type': ''},
                    {'name': 'Asthma', 'type': ''}, {'name': 'Back Problems', 'type': ''},
                    {'name': 'Bleeding Disorder', 'type': ''}, {'name': 'Bipolar Disorder', 'type': ''},
                    {'name': 'Bloot Clot/DVT', 'type': ''},
                    {'name': 'Bypass Surgery', 'type': ''},
                    {'name': 'Cancer', 'type': 'Type'}, {'name': 'Chemical Dependency', 'type': ''},
                    {'name': 'Chest Pain', 'type': ''}, {'name': 'Circulatory Problems', 'type': ''},
                    {'name': 'Depression', 'type': ''},
                    {'name': 'Diabetes', 'type': 'Type' 'How long'}, {'name': 'Emphysema', 'type': ''},
                    {'name': 'Eye Problems', 'type': ''}, {'name': 'Fibromyalgia', 'type': ''},
                    {'name': 'Foot Cramps', 'type': ''}, {'name': 'Gastric Reflux', 'type': ''},
                    {'name': 'Gout', 'type': ''}, {'name': 'Headaches', 'type': ''},
                    {'name': 'Heart Attack', 'type': ''}, {'name': 'Heart Murmur', 'type': ''},
                    ]
        if request.method == 'POST':
            form_data = {'AIDS/HIV': request.form.get('AIDS/HIV'),
                         'Anemia': request.form.get('Anemia'),
                         'Anxiety': request.form.get('Anxiety'),
                         'Arthritis': request.form.get('Arthritis'),
                         'Artificial Heart Valve': request.form.get('Artificial Heart Valve'),
                         'Artificial Joint': request.form.get('Artificial Joint'),
                         'Asthma': request.form.get('Asthma'),
                         'Back Problems': request.form.get('Back Problems'),
                         'Bleeding Disorder': request.form.get('Bleeding Disorder'),
                         'Bipolar Disorder': request.form.get('Bipolar Disorder'),
                         'Blood Clot/DVT': request.form.get('Bloot Clot/DVT'),
                         'Bypass Surgery': request.form.get('Bypass Surgery'),
                         'Cancer': request.form.get('Cancer'),
                         'Chemical Dependency': request.form.get('Chemical Dependency'),
                         'Chest Pain': request.form.get('Chest Pain'),
                         'Circulatory Problems': request.form.get('Circulatory Problems'),
                         'Depression': request.form.get('Depression'),
                         'Diabetes': request.form.get('Diabetes'),
                         'Emphysema': request.form.get('Emphysema'),
                         'Eye Problems': request.form.get('Eye Problems'),
                         'Fibromyalgia': request.form.get('Fibromyalgia'),
                         'Foot Cramps': request.form.get('Foot Cramps'),
                         'Gastric Reflux': request.form.get('Gastric Reflux'),
                         'Gout': request.form.get('Gout'),
                         'Headaches': request.form.get('Headaches'),
                         'Heart Attack': request.form.get('Heart Attack'),
                         'Heart Murmur': request.form.get('Heart Murmur')}
            service.register_information_sheet_1(form_data,

                                                 diseases)
            return redirect(url_for('register_patient_3'))
        return render_template('register_patient_2.html', diseases=diseases, error=error)

    @staticmethod
    @app.route('/edit-information-sheet-1/<patient_id>', methods=['GET', 'POST'])
    def edit_information_sheet_1(patient_id):
        error = None
        diseases = [{'name': 'AIDS/HIV', 'type': ''}, {'name': 'Anemia', 'type': ''}, {'name': 'Anxiety', 'type': ''},
                    {'name': 'Arthritis', 'type': 'Type'},
                    {'name': 'Artificial Heart Valve', 'type': ''}, {'name': 'Artificial Joint', 'type': ''},
                    {'name': 'Asthma', 'type': ''}, {'name': 'Back Problems', 'type': ''},
                    {'name': 'Bleeding Disorder', 'type': ''}, {'name': 'Bipolar Disorder', 'type': ''},
                    {'name': 'Blood Clot/DVT', 'type': ''},
                    {'name': 'Bypass Surgery', 'type': ''},
                    {'name': 'Cancer', 'type': 'Type'}, {'name': 'Chemical Dependency', 'type': ''},
                    {'name': 'Chest Pain', 'type': ''}, {'name': 'Circulatory Problems', 'type': ''},
                    {'name': 'Depression', 'type': ''},
                    {'name': 'Diabetes', 'type': 'Type' 'How long'}, {'name': 'Emphysema', 'type': ''},
                    {'name': 'Eye Problems', 'type': ''}, {'name': 'Fibromyalgia', 'type': ''},
                    {'name': 'Foot Cramps', 'type': ''}, {'name': 'Gastric Reflux', 'type': ''},
                    {'name': 'Gout', 'type': ''}, {'name': 'Headaches', 'type': ''},
                    {'name': 'Heart Attack', 'type': ''}, {'name': 'Heart Murmur', 'type': ''},
                    ]
        if request.method == 'POST':
            form_data = {'AIDS/HIV': request.form.get('AIDS/HIV'),
                         'Anemia': request.form.get('Anemia'),
                         'Anxiety': request.form.get('Anxiety'),
                         'Arthritis': request.form.get('Arthritis'),
                         'Artificial Heart Valve': request.form.get('Artificial Heart Valve'),
                         'Artificial Joint': request.form.get('Artificial Joint'),
                         'Asthma': request.form.get('Asthma'),
                         'Back Problems': request.form.get('Back Problems'),
                         'Bleeding Disorder': request.form.get('Bleeding Disorder'),
                         'Bipolar Disorder': request.form.get('Bipolar Disorder'),
                         'Bloot Clot/DVT': request.form.get('Bloot Clot/DVT'),
                         'Bypass Surgery': request.form.get('Bypass Surgery'),
                         'Cancer': request.form.get('Cancer'),
                         'Chemical Dependency': request.form.get('Chemical Dependency'),
                         'Chest Pain': request.form.get('Chest Pain'),
                         'Circulatory Problems': request.form.get('Circulatory Problems'),
                         'Depression': request.form.get('Depression'),
                         'Diabetes': request.form.get('Diabetes'),
                         'Emphysema': request.form.get('Emphysema'),
                         'Eye Problems': request.form.get('Eye Problems'),
                         'Fibromyalgia': request.form.get('Fibromyalgia'),
                         'Foot Cramps': request.form.get('Foot Cramps'),
                         'Gout': request.form.get('Gout'),
                         'Gastric Reflux': request.form.get('Gastric Reflux'),
                         'Headaches': request.form.get('Headaches'),
                         'Heart Attack': request.form.get('Heart Attack'),
                         'Heart Murmur': request.form.get('Heart Murmur')}
            service.edit_information_sheet_1(form_data, patient_id, diseases)
            return redirect(url_for('edit_information_sheet_2', patient_id=patient_id))
        return render_template('edit-information-sheet-1.html', diseases=diseases, error=error, patient_id=patient_id)

    @staticmethod
    @app.route('/register-patient-3', methods=['GET', 'POST'])
    def register_patient_3():
        error = None
        diseases = [{'name': 'Heart Failure', 'type': ''}, {'name': 'Hemophilia', 'type': ''},
                    {'name': 'Hepatitis', 'type': ''}, {'name': 'High Blood Pressure', 'type': ''},
                    {'name': 'Kidney Problems', 'type': ''},
                    {'name': 'Leg Cramps', 'type': ''},
                    {'name': 'Liver Disease', 'type': ''}, {'name': 'Low Blood Pressure', 'type': ''},
                    {'name': 'Mental Illness', 'type': ''}, {'name': 'Neuropathy', 'type': ''},
                    {'name': 'Pacemaker', 'type': ''},
                    {'name': 'Paralysis', 'type': ''}, {'name': 'Phlebitis', 'type': ''},
                    {'name': 'Psoriasis', 'type': ''}, {'name': 'Rheumatic Fever', 'type': ''},
                    {'name': 'Schizophrenia', 'type': ''}, {'name': 'Shortness of Breath', 'type': ''},
                    {'name': 'Stroke', 'type': ''},
                    {'name': 'Thyroid Problems', 'type': 'Type'},
                    {'name': 'Tuberculosis', 'type': ''}, {'name': 'Ulcers (Stomach)', 'type': ''},
                    {'name': 'Varicose Veins', 'type': ''}, {'name': 'Weight loss(unexplained)', 'type': ''},
                    {'name': 'Pregnant', 'type': ''}, {'name': 'Breastfeeding', 'type': ''}
                    ]
        if request.method == 'POST':
            form_data = {'Heart Failure': request.form.get('Heart Failure'),
                         'Hemophilia': request.form.get('Hemophilia'),
                         'Hepatitis': request.form.get('Hepatitis'),
                         'High Blood Pressure': request.form.get('High Blood Pressure'),
                         'Kidney Problems': request.form.get('Kidney Problems'),
                         'Leg Cramps': request.form.get('Leg Cramps'),
                         'Liver Disease': request.form.get('Liver Disease'),
                         'Low Blood Pressure': request.form.get('Low Blood Pressure'),
                         'Mental Illness': request.form.get('Mental Illness'),
                         'Neuropathy': request.form.get('Neuropathy'),
                         'Pacemaker': request.form.get('Pacemaker'),
                         'Paralysis': request.form.get('Paralysis'),
                         'Phlebitis': request.form.get('Phlebitis'),
                         'Psoriasis': request.form.get('Psoriasis'),
                         'Rheumatic Fever': request.form.get('Rheumatic Fever'),
                         'Schizophrenia': request.form.get('Schizophrenia'),
                         'Shortness of Breath': request.form.get('Shortness of Breath'),
                         'Stroke': request.form.get('Stroke'),
                         'Thyroid Problems': request.form.get('Thyroid Problems'),
                         'Tuberculosis': request.form.get('Tuberculosis'),
                         'Ulcers (Stomach)': request.form.get('Ulcers (Stomach)'),
                         'Varicose Veins': request.form.get('Varicose Veins'),
                         'Weight loss': request.form.get('Weight loss'),
                         'Pregnant': request.form.get('Pregnant'),
                         'Breastfeeding': request.form.get('Breastfeeding')}
            service.register_information_sheet_2(form_data, diseases)
            return redirect(url_for('register_patient_4'))
        return render_template('register_patient_3.html', diseases=diseases, error=error)

    @staticmethod
    @app.route('/edit-information-sheet-2/<patient_id>', methods=['GET', 'POST'])
    def edit_information_sheet_2(patient_id):
        error = None
        diseases = [{'name': 'Heart Failure', 'type': ''}, {'name': 'Hemophilia', 'type': ''},
                    {'name': 'Hepatitis', 'type': ''}, {'name': 'High Blood Pressure', 'type': ''},
                    {'name': 'Kidney Problems', 'type': ''},
                    {'name': 'Leg Cramps', 'type': ''},
                    {'name': 'Liver Disease', 'type': ''}, {'name': 'Low Blood Pressure', 'type': ''},
                    {'name': 'Mental Illness', 'type': ''}, {'name': 'Neuropathy', 'type': ''},
                    {'name': 'Pacemaker', 'type': ''},
                    {'name': 'Paralysis', 'type': ''}, {'name': 'Phlebitis', 'type': ''},
                    {'name': 'Psoriasis', 'type': ''}, {'name': 'Rheumatic Fever', 'type': ''},
                    {'name': 'Schizophrenia', 'type': ''}, {'name': 'Shortness of Breath', 'type': ''},
                    {'name': 'Stroke', 'type': ''},
                    {'name': 'Thyroid Problems', 'type': 'Type'},
                    {'name': 'Tuberculosis', 'type': ''}, {'name': 'Ulcers (Stomach)', 'type': ''},
                    {'name': 'Varicose Veins', 'type': ''}, {'name': 'Weight loss', 'type': ''},
                    {'name': 'Pregnant', 'type': ''}, {'name': 'Breastfeeding', 'type': ''}
                    ]
        if request.method == 'POST':
            form_data = {'Heart Failure': request.form.get('Heart Failure'),
                         'Hemophilia': request.form.get('Hemophilia'),
                         'Hepatitis': request.form.get('Hepatitis'),
                         'High Blood Pressure': request.form.get('High Blood Pressure'),
                         'Kidney Problems': request.form.get('Kidney Problems'),
                         'Leg Cramps': request.form.get('Leg Cramps'),
                         'Liver Disease': request.form.get('Liver Disease'),
                         'Low Blood Pressure': request.form.get('Low Blood Pressure'),
                         'Mental Illness': request.form.get('Mental Illness'),
                         'Neuropathy': request.form.get('Neuropathy'),
                         'Pacemaker': request.form.get('Pacemaker'),
                         'Paralysis': request.form.get('Paralysis'),
                         'Phlebitis': request.form.get('Phlebitis'),
                         'Psoriasis': request.form.get('Psoriasis'),
                         'Rheumatic Fever': request.form.get('Rheumatic Fever'),
                         'Schizophrenia': request.form.get('Schizophrenia'),
                         'Shortness of Breath': request.form.get('Shortness of Breath'),
                         'Stroke': request.form.get('Stroke'),
                         'Thyroid Problems': request.form.get('Thyroid Problems'),
                         'Tuberculosis': request.form.get('Tuberculosis'),
                         'Ulcers (Stomach)': request.form.get('Ulcers (Stomach)'),
                         'Varicose Veins': request.form.get('Varicose Veins'),
                         'Weight loss': request.form.get('Weight loss'),
                         'Pregnant': request.form.get('Pregnant'),
                         'Breastfeeding': request.form.get('Breastfeeding')}
            service.edit_information_sheet_2(form_data, patient_id, diseases)
            return redirect(url_for('edit_information_sheet_3',patient_id=patient_id))
        return render_template('edit-information-sheet-2.html', diseases=diseases, error=error, patient_id=patient_id)

    @staticmethod
    @app.route('/register-patient-4', methods=['GET', 'POST'])
    def register_patient_4():
        error = None
        allergies = [
            {'name': 'Local anesthesia'}, {'name': 'Aspirin'}, {'name': 'Anti-Inflammatory'}, {'name': 'Penicillin'},
            {'name': 'Sulfa'}, {'name': 'IVP dye'}, {'name': 'Tetanus'}, {'name': 'General anesthesia'},
            {'name': 'Latex'}, {'name': 'Tape/Adhesives'}, {'name': 'Iodine'}, {'name': 'Betadine'},
            {'name': 'Codeine'}, {'name': 'Steroids'}
        ]
        if request.method == 'POST':
            form_data = {'Local anesthesia': request.form.get('Local anesthesia'),
                         'Aspirin': request.form.get('Aspirin'),
                         'Anti-Inflammatory': request.form.get('Anti-Inflammatory'),
                         'Penicillin': request.form.get('Penicillin'),
                         'Sulfa': request.form.get('Sulfa'),
                         'IVP dye': request.form.get('IVP dye'),
                         'Tetanus': request.form.get('Tetanus'),
                         'General anesthesia': request.form.get('General anesthesia'),
                         'Latex': request.form.get('Latex'),
                         'Tape/Adhesives': request.form.get('Tape/Adhesives'),
                         'Iodine': request.form.get('Iodine'),
                         'Betadine': request.form.get('Betadine'),
                         'Codeine': request.form.get('Codeine'),
                         'Steroids': request.form.get('Steroids')}
            service.register_information_sheet_3(form_data, allergies)
            return redirect(url_for('register_patient_5'))
        return render_template('register_patient_4.html', allergies=allergies, error=error)


    @staticmethod
    @app.route('/edit-information-sheet-3/<patient_id>', methods=['GET', 'POST'])
    def edit_information_sheet_3(patient_id):
        error = None
        allergies = [
            {'name': 'Local anesthesia'}, {'name': 'Aspirin'}, {'name': 'Anti-Inflammatory'}, {'name': 'Penicillin'},
            {'name': 'Sulfa'}, {'name': 'IVP dye'}, {'name': 'Tetanus'}, {'name': 'General anesthesia'},
            {'name': 'Latex'}, {'name': 'Tape/Adhesives'}, {'name': 'Iodine'}, {'name': 'Betadine'},
            {'name': 'Codeine'}, {'name': 'Steroids'}
        ]
        if request.method == 'POST':
            form_data = {'Local anesthesia': request.form.get('Local anesthesia'),
                         'Aspirin': request.form.get('Aspirin'),
                         'Anti-Inflammatory': request.form.get('Anti-Inflammatory'),
                         'Penicillin': request.form.get('Penicillin'),
                         'Sulfa': request.form.get('Sulfa'),
                         'IVP dye': request.form.get('IVP dye'),
                         'Tetanus': request.form.get('Tetanus'),
                         'General anesthesia': request.form.get('General anesthesia'),
                         'Latex': request.form.get('Latex'),
                         'Tape/Adhesives': request.form.get('Tape/Adhesives'),
                         'Iodine': request.form.get('Iodine'),
                         'Betadine': request.form.get('Betadine'),
                         'Codeine': request.form.get('Codeine'),
                         'Steroids': request.form.get('Steroids')}
            service.edit_information_sheet_3(form_data, patient_id, allergies)
            return redirect(url_for('edit_information_sheet_4', patient_id=patient_id))
        return render_template('edit-information-sheet-3.html', allergies=allergies, error=error)

    @staticmethod
    @app.route('/register-patient-5', methods=['GET', 'POST'])
    def register_patient_5():
        error = None
        if request.method == 'POST':
            form_data = [request.form['weight'],
                         request.form['height'],
                         request.form['shoe_size'],
                         request.form['medications'],
                         request.form['hospitalization'],
                         request.form.get('smoking'),
                         request.form.get('drinking'),
                         request.form['blood_type']]
            try:
                service.register_information_sheet_4(form_data)
            except ValueError as exception:
                error = exception
            else:
                service.link_patient_to_information_sheet()
                return redirect(url_for('login'))
        return render_template('register_patient_5.html', error=error)

    @staticmethod
    @app.route('/edit-information-sheet-4/<patient_id>', methods=['GET', 'POST'])
    def edit_information_sheet_4(patient_id):
        error = None
        if request.method == 'POST':
            form_data = [request.form['weight'],
                         request.form['height'],
                         request.form['shoe_size'],
                         request.form['medications'],
                         request.form['hospitalization'],
                         request.form.get('smoking'),
                         request.form.get('drinking'),
                         request.form['blood_type']]
            service.edit_information_sheet_4(form_data, patient_id)
            return redirect(url_for('patient_information_sheet', patient_id=patient_id))
        return render_template('edit-information-sheet-4.html', error=error)

    @staticmethod
    @app.route('/choice')
    def choice():
        return render_template('choice.html')

    @staticmethod
    @app.route('/medic-home')
    def medic_home():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('medic-home.html')

    @staticmethod
    @app.route('/patient-home')
    def patient_home():
        if "patient" not in service.session:
            return redirect(url_for('home'))
        patient_id = service.session['patient']
        patient = service.get_patient_by_id(patient_id)
        doctor_id = patient.doctor_id
        doctor = service.get_doctor_by_id(doctor_id)
        return render_template('patient-home.html', doctor=doctor)

    @staticmethod
    @app.route('/patient-list')
    def patient_list():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        patients = service.get_doctor_patients()
        # patients = db.find_all_doctors_ids()
        return render_template('patient-list.html', patients=patients)

    @staticmethod
    @app.route('/transfer-patients')
    def transfer_patients():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        patients = service.get_patients_that_want_to_transfer()
        return render_template('transfer-patients.html', patients=patients)

    """@app.route('/transfer-patients')
    def transfer_patients():
        error = None
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        if request.method == 'POST':
            patient_id = request.form['patient_id']
            doctor_id = request.form['doctor_id']
            service.transfer_patient(patient_id, doctor_id)
            return redirect(url_for('transfer_patients'))
        patients = service.get_patients_that_want_to_transfer()
        doctors = service.get_all_doctors()
        return render_template('transfer-patients.html', patients=patients, doctors=doctors)"""

    @staticmethod
    @app.route('/invite-patient')
    def invite_patient():
        if "doctor" not in service.session:
            return redirect(url_for('home'))

        return render_template('invite-patient.html')

    @staticmethod
    @app.route('/medic-profile')
    def medic_profile():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        doctor = service.get_doctor_by_id(service.session['doctor'])
        return render_template('medic-profile.html', doctor=doctor)

    @staticmethod
    @app.route('/patient-profile')
    def patient_profile():
        if "patient" not in service.session:
            return redirect(url_for('home'))
        patient = service.get_patient_by_id(service.session['patient'])
        return render_template('patient-profile.html', patient=patient)

    @staticmethod
    @app.route('/edit-medic', methods=['GET', 'POST'])
    def edit_medic():
        error = None
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        if request.method == "POST":
            doctor = service.get_doctor_by_id(service.session['doctor'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'],
                         request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password'], request.form['gender'],
                         request.form['zipcode'], request.form['city'],
                         request.form['county'],
                         request.files['profile_picture']]
            try:
                service.update_doctor_profile(doctor, form_data)
            except ValueError as exception:
                error = exception
            else:
                service.update_database()
                return redirect(url_for('medic_profile'))
        return render_template('edit-medic.html', error=error)

    @staticmethod
    @app.route('/edit-patient', methods=['GET', 'POST'])
    def edit_patient():
        error = None
        if "patient" not in service.session:
            return redirect(url_for('home'))
        if request.method == "POST":
            patient = service.get_patient_by_id(service.session['patient'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['zipcode'], request.form['city'],
                         request.form['county'], request.form['passport_id'],
                         request.form['birth_date'], request.form['marital_status'],
                         request.form['gender'], request.form['occupation'], request.form['password'],
                         request.files['profile_picture']]
            try:
                service.update_patient_profile(patient, form_data)
            except ValueError as exception:
                error = exception
            else:
                service.update_database()
                return redirect(url_for('patient_profile'))
        return render_template('edit-patient.html', error=error)

    @staticmethod
    @app.route('/patient/<patient_id>')
    def patient(patient_id):
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        patient = service.get_patient_by_id(patient_id)
        return render_template('patient.html', patient=patient)

    @staticmethod
    @app.route('/consultation-history')
    def consultation_history():
        if "patient" not in service.session:
            return redirect(url_for('home'))
        patient_id = service.session['patient']
        medical_history = service.get_consultation_history(patient_id)
        return render_template('medical-history.html', medical_history=medical_history)

    @staticmethod
    @app.route('/patient-consultation-history/<patient_id>')
    def patient_consultation_history(patient_id):
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        medical_history = service.get_consultation_history(patient_id)
        return render_template('patient-medical-history.html', patient_id=patient_id, medical_history=medical_history)

    @staticmethod
    @app.route('/change-medic', methods=['GET', 'POST'])
    def change_medic():
        if "patient" not in service.session:
            return redirect(url_for('home'))
        patient_id = service.session['patient']
        patient = service.get_patient_by_id(patient_id)
        current_doctor = service.get_doctor_by_id(patient.doctor_id)
        doctors = service.get_doctors_nearby_patient(patient_id)
        if request.method == "POST":
            rating = request.form['rating']
            service.add_rating(rating)
        return render_template('change-medic.html', current_doctor=current_doctor, doctors=doctors, patient=patient)

    @staticmethod
    @app.route('/consultation/file/<filename>')
    def uploaded_consultation(filename):
        path = os.path.abspath(os.path.join(app.root_path, 'static/files/consultation', filename))
        if os.path.exists(path):
            return send_from_directory(os.path.abspath(os.path.join(app.root_path, 'static/files/consultation')),
                                       filename)
        else:
            return render_template('error.html', error_message='No pdf uploaded'), 404

    @staticmethod
    @app.errorhandler(404)
    def not_found_error():
        return render_template('error.html', error_message='Page not found'), 404

    @staticmethod
    @app.route('/invite-patient', methods=['GET', 'POST'])
    def invitation():
        if "doctor" not in service.session:
            return redirect(url_for('home'))

        destination_number = '+40772093773'
        if request.method == 'POST':
            if request.form['phone_number'] == '+4007720937733':
                service.send_welcome_sms(destination_number)
                message = 'Invite sent!'
                return render_template('invite-patient.html', message=message)
            else:
                error = 'Wrong credentials. Try again.'
                return render_template('invite-patient.html', error=error)
        else:
            return render_template('invite-patient.html')

    @staticmethod
    @app.route('/information-sheet')
    def information_sheet():
        if "patient" not in service.session:
            return redirect(url_for('home'))
        patient_id = service.session['patient']
        patient = service.get_patient_by_id(patient_id)
        information_sheet = service.get_information_sheet_by_patient_id(service.session['patient'])
        return render_template('information-sheet.html', patient=patient, information_sheet=information_sheet)

    @staticmethod
    @app.route('/patient-information-sheet/<patient_id>')
    def patient_information_sheet(patient_id):
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        patient = service.get_patient_by_id(patient_id)
        information_sheet = service.get_information_sheet_by_patient_id(patient_id)
        return render_template('patient-information-sheet.html', patient=patient, information_sheet=information_sheet)

    @staticmethod
    @app.route('/approve-transfer/<patient_id>/<doctor_id>', methods=['POST'])
    def approve_transfer(patient_id, doctor_id):
        data = request.get_json()
        confirmed = data['confirmed']
        if confirmed:
            service.transfer_patient(patient_id, doctor_id)
        return 'OK'

    @staticmethod
    @app.route('/create-transfer/<doctor_id>', methods=['POST'])
    def create_transfer(doctor_id):
        data = request.get_json()
        confirmed = data['confirmed']
        if confirmed:
            try:
                service.request_transfer(doctor_id)
            except Exception as error:
                return str(error), 400
        return 'OK', 200

    @staticmethod
    @app.route('/consultation/<consultation_id>', methods=['GET', 'POST'])
    def consultation(consultation_id):
        consultation_pdf = service.get_consultation(consultation_id).pdf
        error = None
        if request.method == 'POST':
            pdf = request.files['pdf']
            if pdf.filename == "":
                error = "File not uploaded"
            else:
                service.add_pdf_to_consultation(consultation_id, pdf)
                service.update_database()
                flask.flash("Uploaded successfully")
                return redirect(url_for('consultation', consultation_id=consultation_id))
        return render_template('consultation.html', consultation_pdf=consultation_pdf, error=error)
