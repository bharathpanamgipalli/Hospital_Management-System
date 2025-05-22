from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import Doctor
from models import db, User, Patient, Appointment, Medicine, DoctorSchedule

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def before_request_func():
    print("Flask app received a request.")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = user.username
        session['role'] = user.role
        return redirect("/dashboard")
    return "Login Failed!"

@app.route("/dashboard")
def dashboard():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    schedules = DoctorSchedule.query.all()
    medicines = Medicine.query.all()
    return render_template("dashboard.html", patients=patients, doctors=doctors, schedules=schedules, medicines=medicines)

# ADD Patient
@app.route("/add_patient", methods=["POST"])
def add_patient():
    name = request.form["name"]
    contact = request.form["contact"]
    history = request.form["history"]
    patient = Patient(name=name, contact=contact, history=history)
    db.session.add(patient)
    db.session.commit()
    return redirect("/dashboard")

# DELETE Patient
@app.route("/delete_patient/<int:id>", methods=["POST"])
def delete_patient(id):
    patient = Patient.query.get(id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect("/dashboard")

# ADD Doctor and Schedule
@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    doctor = request.form["doctor_name"]
    days = request.form["available_days"]
    timings = request.form["timings"]
    schedule = DoctorSchedule(doctor_name=doctor, available_days=days, timings=timings)
    db.session.add(schedule)
    db.session.commit()
    return redirect("/dashboard")

# DELETE Doctor
@app.route("/delete_doctor/<int:id>", methods=["POST"])
def delete_doctor(id):
    doc = DoctorSchedule.query.get(id)
    if doc:
        db.session.delete(doc)
        db.session.commit()
    return redirect("/dashboard")

# ADD Medicine
@app.route("/add_medicine", methods=["POST"])
def add_medicine():
    name = request.form["name"]
    quantity = request.form["quantity"]
    med = Medicine(name=name, quantity=quantity)
    db.session.add(med)
    db.session.commit()
    return redirect("/dashboard")

# DELETE Medicine
@app.route("/delete_medicine/<int:id>", methods=["POST"])
def delete_medicine(id):
    med = Medicine.query.get(id)
    if med:
        db.session.delete(med)
        db.session.commit()
    return redirect("/dashboard")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        history = request.form["history"]
        new_patient = Patient(name=name, contact=contact, history=history)
        db.session.add(new_patient)
        db.session.commit()
        return redirect("/dashboard")
    return render_template("register.html")

@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    if request.method == "POST":
        patient = request.form["patient"]
        doctor = request.form["doctor"]
        date = request.form["date"]
        time = request.form["time"]
        new_appointment = Appointment(patient_name=patient, doctor_name=doctor, date=date, time=time)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect("/dashboard")
    
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template("appointment.html", patients=patients, doctors=doctors)

@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        new_item = Medicine(name=name, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return redirect("/dashboard")
    medicines = Medicine.query.all()
    return render_template("inventory.html", medicines=medicines)

@app.route("/doctor_schedule", methods=["GET", "POST"])
def doctor_schedule():
    if request.method == "POST":
        name = request.form["doctor"]
        days = request.form["days"]
        timings = request.form["timings"]
        new_schedule = DoctorSchedule(doctor_name=name, available_days=days, timings=timings)
        db.session.add(new_schedule)
        db.session.commit()
        return redirect("/dashboard")
    doctors = Doctor.query.all()
    schedules = DoctorSchedule.query.all()
    return render_template("doctor_schedule.html", doctors=doctors, schedules=schedules)

if __name__ == "__main__":
    app.secret_key = 'your_secret_key'
    with app.app_context():
        db.create_all()
    app.run(debug=True)
