from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        new_patient = Patient(name=name, age=age, gender=gender)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_patient.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', patient=patient)

@app.route('/delete/<int:id>')
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

#-------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)

@app.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        new_employee = Employee(name=name, position=position)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('employees'))
    return render_template('add_employee.html')

#--------
# Модель данных для управления расписанием
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Маршруты для управления расписанием
@app.route('/appointments')
def appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date_str = request.form['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('appointments'))
    return render_template('add_appointment.html')

# Модель данных для электронной медицинской карты
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(100), nullable=False)

# Маршруты для электронной медицинской карты
@app.route('/medical_records/<int:patient_id>')
def medical_records(patient_id):
    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
    return render_template('medical_records.html', records=records)

@app.route('/medical_records/add/<int:patient_id>', methods=['GET', 'POST'])
def add_medical_record(patient_id):
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        new_record = MedicalRecord(patient_id=patient_id, diagnosis=diagnosis, treatment=treatment)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('medical_records', patient_id=patient_id))
    return render_template('add_medical_record.html')

# --------
# Модель данных для онлайн-консультаций
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Маршруты для онлайн-консультаций
@app.route('/consultations')
def consultations():
    consultations = Consultation.query.all()
    return render_template('consultations.html', consultations=consultations)

@app.route('/consultations/add', methods=['GET', 'POST'])
def add_consultation():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date_str = request.form['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        new_consultation = Consultation(patient_id=patient_id, doctor_id=doctor_id, date=date)
        db.session.add(new_consultation)
        db.session.commit()
        return redirect(url_for('consultations'))
    return render_template('add_consultation.html')

# Модель данных для онлайн-оплаты
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Маршруты для онлайн-оплаты
@app.route('/payments')
def payments():
    payments = Payment.query.all()
    return render_template('payments.html', payments=payments)

@app.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']
        date_str = request.form['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        new_payment = Payment(patient_id=patient_id, amount=amount, date=date)
        db.session.add(new_payment)
        db.session.commit()
        return redirect(url_for('payments'))
    return render_template('add_payment.html')

# -----------
# Модель данных для уведомлений и напоминаний
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Маршруты для уведомлений и напоминаний
@app.route('/notifications')
def notifications():
    notifications = Notification.query.all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/notifications/add', methods=['GET', 'POST'])
def add_notification():
    if request.method == 'POST':
        recipient_id = request.form['recipient_id']
        message = request.form['message']
        date_str = request.form['date']
        print(f"recipient_id: {recipient_id}, message: {message}, date_str: {date_str}") 
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        new_notification = Notification(recipient_id=recipient_id, message=message, date=date)
        db.session.add(new_notification)
        db.session.commit()
        return redirect(url_for('notifications'))
    return render_template('add_notification.html')

# Маршрут для отчетов
@app.route('/reports')
def reports():
    data = {
        'Всего пациентов': Patient.query.count(),
        'Общее количество сотрудников': Employee.query.count(),
        'Общее количество назначений': Appointment.query.count(),
        'Общее количество консультаций': Consultation.query.count(),
        'Всего было платежей': Payment.query.count(),
        'Общее количество уведомлений': Notification.query.count(),
    }
    return render_template('reports.html', data=data)

@app.route('/patients')
def patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



