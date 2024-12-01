from app import app, db
from app.domain.entities import Patient, Doctor, Consultation
from app.ui.ui import Routes

if __name__ == '__main__':
    app.run(debug=True)
    routes = Routes()


    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'Consultation': Consultation}
