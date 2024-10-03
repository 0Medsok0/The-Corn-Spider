from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)


@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    new_patient = Patient(name=name, age=age, gender=gender)
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('index'))

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
    # добавьте дополнительные поля по необходимости

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
    # добавьте дополнительные поля по необходимости

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
        date = request.form['date']
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
    # добавьте дополнительные поля по необходимости

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
    # добавьте дополнительные поля по необходимости

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
        date = request.form['date']
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
    # добавьте дополнительные поля по необходимости

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
        date = request.form['date']
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
    # добавьте дополнительные поля по необходимости

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
        date = request.form['date']
        new_notification = Notification(recipient_id=recipient_id, message=message, date=date)
        db.session.add(new_notification)
        db.session.commit()
        return redirect(url_for('notifications'))
    return render_template('add_notification.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

