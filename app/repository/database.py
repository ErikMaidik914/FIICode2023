import datetime
from cgitb import text

from app.domain.entities import Doctor, Patient, Consultation, ChronicDisease, Allergy, \
    Hospitalization, InformationSheet, InviteCode, information_sheet_chronic_disease, information_sheet_allergy


class Database:

    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def add_entity(self, entity):
        self.db.session.add(entity)

    def find_doctor_by_id(self, doctor_id):
        doctor = self.db.session.get(Doctor, doctor_id)
        if doctor is None:
            raise ValueError("Doctor not found")
        return doctor

    def find_consultation_by_id(self, consultation_id):
        consultation = self.db.session.get(Consultation, consultation_id)
        if consultation is None:
            raise ValueError("Consultation not found")
        return consultation

    def find_information_sheet_by_id(self, information_sheet_id):
        information_sheet = self.db.session.get(InformationSheet, information_sheet_id)
        if information_sheet is None:
            raise ValueError("Information sheet not found")
        return information_sheet

    def find_patient_by_id(self, patient_id):
        patient = self.db.session.get(Patient, patient_id)
        if patient is None:
            raise ValueError("Patient not found")
        return patient

    def find_invite_code(self, code):
        invite = None
        for invite_code in self.find_all_invite_codes():
            if invite_code.invite_code == code:
                invite = invite_code
        if invite is None:
            raise ValueError("Invite code not found")
        return invite

    @staticmethod
    def find_all_doctors():
        return Doctor.query.all()

    @staticmethod
    def find_all_patients():
        return Patient.query.all()

    @staticmethod
    def find_all_consultations():
        return Consultation.query.all()

    @staticmethod
    def find_all_invite_codes():
        return InviteCode.query.all()

    def find_all_doctors_ids(self):
        ids = []
        for doctor in self.find_all_doctors():
            ids.append(doctor.id)
        return ids

    def find_all_patients_ids(self):
        ids = []
        for patient in self.find_all_patients():
            ids.append(patient.id)
        return ids

    def save_to_database(self):
        self.db.session.commit()

    def clear_patients_table(self):
        self.db.session.query(Patient).delete()
        self.db.session.commit()

    def clear_doctors_table(self):
        self.db.session.query(Doctor).delete()
        self.db.session.commit()

    def clear_consultation_table(self):
        self.db.session.query(Consultation).delete()
        self.db.session.commit()

    def clear_invite_code_table(self):
        self.db.session.query(InviteCode).delete()
        self.db.session.commit()

    def clear_allergy_table(self):
        self.db.session.query(Allergy).delete()
        self.db.session.commit()

    def clear_chronic_disease_table(self):
        self.db.session.query(ChronicDisease).delete()
        self.db.session.commit()

    def clear_table_1(self):
        self.db.session.query(information_sheet_chronic_disease).delete()
        self.db.session.commit()

    def clear_table_2(self):
        self.db.session.query(information_sheet_allergy).delete()
        self.db.session.commit()

    @staticmethod
    def find_doctor_username(username):
        doctor = Doctor.query.filter_by(username=username).first()
        return doctor

    @staticmethod
    def find_patient_username(username):
        patient = Patient.query.filter_by(username=username).first()
        return patient

    @staticmethod
    def find_disease_by_name(name):
        disease = ChronicDisease.query.filter_by(name=name).first()
        if disease is None:
            raise ValueError("No disease found")
        return disease

    @staticmethod
    def find_allergy_by_name(name):
        allergy = Allergy.query.filter_by(name=name).first()
        if allergy is None:
            raise ValueError("Allergy not found")
        return allergy

    @staticmethod
    def find_all_chronic_diseases():
        return ChronicDisease.query.all()

    @staticmethod
    def find_all_allergies():
        return Allergy.query.all()

    def clear_hospitalization_table(self):
        self.db.session.query(Hospitalization).delete()
        self.db.session.commit()

    def clear_information_sheet_table(self):
        self.db.session.query(InformationSheet).delete()
        self.db.session.commit()

    def remove_consultation(self, consultation_id):
        consultation = self.find_consultation_by_id(consultation_id)
        if consultation is None:
            raise ValueError("Consultation not found")
        consultation.remove()
        self.db.session.commit()

    def remove_patient(self, patient_id):
        patient = self.find_patient_by_id(patient_id)
        if patient is None:
            raise ValueError("Patient not found")
        patient.remove()
        self.db.session.commit()

    def remove_information_sheet(self, information_sheet_id):
        information_sheet = self.find_information_sheet_by_id(information_sheet_id)
        if information_sheet is None:
            raise ValueError("Information sheet not found")
        information_sheet.remove()
        self.db.session.commit()

    def remove_doctor(self, doctor_id):
        doctor = self.find_doctor_by_id(doctor_id)
        if doctor is None:
            raise ValueError("Doctor not found")
        doctor.remove()
        self.db.session.commit()
