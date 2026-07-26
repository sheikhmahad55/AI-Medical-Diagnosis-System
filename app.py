from flask import Flask, render_template, request, redirect, session
from datetime import datetime
# from flask_migrate import history
import joblib
# from matplotlib import table
# from matplotlib.table import table
import numpy as np
from config import Config
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import io
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
# from reportlab.platypus import Image


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///medical.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = "aimedcare123"
app.config.from_object(Config)
model = joblib.load("models/diabetes_model.pkl")

class Prediction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    glucose = db.Column(db.Float)
    bloodpressure = db.Column(db.Float)
    bmi = db.Column(db.Float)
    insulin = db.Column(db.Float)

    risk = db.Column(db.Integer)

    prediction = db.Column(db.String(30))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/how-it-works")
def how_it_works():
    return render_template("how-it-works.html")


@app.route("/diagnosis")
def diagnosis():
    return render_template("diagnosis.html")


@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/result")
def result():

    patient = session.get("patient")

    if not patient:
        return redirect("/diagnosis")

    if patient["prediction"] == 1:
        return render_template(
            "result-positive.html",
            patient=patient
        )

    return render_template(
        "result-negative.html",
        patient=patient
    )

@app.route("/result-positive")
def result_positive():
    return render_template("result-positive.html")


@app.route("/result-negative")
def result_negative():
    return render_template("result-negative.html")


@app.route("/report")
def report():

    patient = session.get("patient")

    if not patient:
        return redirect("/diagnosis")

    current_date = datetime.now().strftime("%d %B %Y")

    return render_template(
        "report.html",
        patient=patient,
        current_date=current_date
    )

@app.route("/history")
def history():
    if not session.get("admin"):
        return redirect("/admin-login")

    patients = Prediction.query.order_by(Prediction.id.desc()).all()

    return render_template(
        "history.html",
        patients=patients
    )

@app.route("/admin-login")
def admin_login():
    return render_template("admin-login.html")

@app.route("/admin-auth", methods=["POST"])
def admin_auth():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":

        session["admin"] = True

        return redirect("/dashboard")

    return render_template(
        "admin-login.html",
        error="Invalid Username or Password"
    )

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/admin-login")


@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect("/admin-login")

    patient = Prediction.query.get_or_404(id)

    db.session.delete(patient)

    db.session.commit()

    return redirect("/history")


@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin-login")

    total = Prediction.query.count()

    high = Prediction.query.filter_by(
        prediction="High Risk"
    ).count()

    low = Prediction.query.filter_by(
        prediction="Low Risk"
    ).count()

    avg_risk = db.session.query(
        db.func.avg(Prediction.risk)
    ).scalar()

    if avg_risk is None:
        avg_risk = 0

    # ==========================
    # Male / Female Count
    # ==========================

    male = Prediction.query.filter_by(
        gender="Male"
    ).count()

    female = Prediction.query.filter_by(
        gender="Female"
    ).count()

    # ==========================
    # Age Groups
    # ==========================

    age20 = Prediction.query.filter(
        Prediction.age.between(20, 30)
    ).count()

    age31 = Prediction.query.filter(
        Prediction.age.between(31, 40)
    ).count()

    age41 = Prediction.query.filter(
        Prediction.age.between(41, 50)
    ).count()

    age51 = Prediction.query.filter(
        Prediction.age.between(51, 60)
    ).count()

    age60 = Prediction.query.filter(
        Prediction.age > 60
    ).count()

    # ==========================
    # Recent Patients
    # ==========================

    recent = Prediction.query.order_by(
        Prediction.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",

        total=total,
        high=high,
        low=low,
        avg_risk=round(avg_risk),

        male=male,
        female=female,

        age20=age20,
        age31=age31,
        age41=age41,
        age51=age51,
        age60=age60,

        recent=recent
    )
    

# @app.route("/download-pdf")
# def download_pdf():

#     patient = session.get("patient")

#     if not patient:
#         return redirect("/diagnosis")

#     return send_file(
#         "static/sample-report.pdf",
#         as_attachment=True
#     )
    
@app.route("/predict", methods=["POST"])
def predict():

    pregnancies = float(request.form["Pregnancies"])
    glucose = float(request.form["Glucose"])
    bloodpressure = float(request.form["BloodPressure"])
    skinthickness = float(request.form["SkinThickness"])
    insulin = float(request.form["Insulin"])
    bmi = float(request.form["BMI"])
    dpf = float(request.form["DiabetesPedigreeFunction"])
    age = int(request.form["Age"])

    data = np.array([[pregnancies,
                      glucose,
                      bloodpressure,
                      skinthickness,
                      insulin,
                      bmi,
                      dpf,
                      age]])

    prediction = model.predict(data)
    probability = model.predict_proba(data)[0][1]
    risk = round(probability * 100)

    patient = {
        "name": request.form.get("patientName") or "Patient",
        "age": age,
        "gender": request.form.get("gender") or "Not Selected",

        "bmi": bmi,
        "glucose": glucose,
        "bloodpressure": bloodpressure,
        "insulin": insulin,
        "risk": risk,

        # Model prediction (0 or 1)
        "prediction": int(prediction[0]),

        # Display text
        "prediction_text": "High Risk" if prediction[0] == 1 else "Low Risk",

        # Health status
        "health": "Needs Attention" if prediction[0] == 1 else "Healthy"
    }

    # Save prediction history
    try:
        history = pd.read_csv("dataset/diabetes.csv")
    except:
        history = pd.DataFrame()

    new_data = pd.DataFrame([{
        "Name": patient["name"],
        "Age": patient["age"],
        "Gender": patient["gender"],
        "Glucose": patient["glucose"],
        "BMI": patient["bmi"],
        "Insulin": patient["insulin"],
        "BloodPressure": patient["bloodpressure"],
        "Risk": patient["risk"],
        "Prediction": patient["prediction_text"]
    }])

    history = pd.concat([history, new_data], ignore_index=True)
    history.to_csv("dataset/diabetes.csv", index=False)

    # Save to Database
    new_prediction = Prediction(
        name=patient["name"],
        age=patient["age"],
        gender=patient["gender"],
        glucose=patient["glucose"],
        bloodpressure=patient["bloodpressure"],
        bmi=patient["bmi"],
        insulin=patient["insulin"],
        risk=patient["risk"],
        prediction=patient["prediction_text"]
    )

    db.session.add(new_prediction)
    db.session.commit()

    session["patient"] = patient

    return redirect("/loading") 


@app.route("/download-pdf")
def download_pdf():

    patient = session.get("patient")

    if not patient:
        return redirect("/diagnosis")

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    # ==========================
    # Header
    # ==========================

    story.append(
        Paragraph(
            "<font size=22 color='darkblue'><b>AI MedCare</b></font>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "<font size=16><b>Medical Diagnosis Report</b></font>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Report Date: {datetime.now().strftime('%d %B %Y')}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    # ==========================
    # Patient Information
    # ==========================

    story.append(
        Paragraph(
            "<font size=15 color='darkgreen'><b>Patient Information</b></font>",
            styles["Heading2"]
        )
    )

    data = [
        ["Parameter", "Value"],
        ["Name", patient["name"]],
        ["Age", str(patient["age"])],
        ["Gender", patient["gender"]],
        ["BMI", str(patient["bmi"])],
        ["Glucose", f"{patient['glucose']} mg/dL"],
        ["Blood Pressure", f"{patient['bloodpressure']} mmHg"],
        ["Insulin", str(patient["insulin"])],
        ["Risk Score", f"{patient['risk']}%"],
        ["Prediction", patient["prediction_text"]],
        ["Health Status", patient["health"]],
    ]

    table = Table(data, colWidths=[180, 220])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), "#1E88E5"),
        ("TEXTCOLOR", (0, 0), (-1, 0), "white"),
        ("GRID", (0, 0), (-1, -1), 1, "black"),
        ("BACKGROUND", (0, 1), (-1, -1), "#F5F5F5"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
    ]))

    story.append(table)

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    # ==========================
    # Medical Analysis
    # ==========================

    story.append(
        Paragraph(
            "<font size=15 color='darkred'><b>Medical Analysis</b></font>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"""
            <b>AI Prediction:</b> {patient['prediction_text']}<br/>
            <b>Risk Score:</b> {patient['risk']}%<br/>
            <b>Health Status:</b> {patient['health']}
            """,
            styles["BodyText"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    # ==========================
    # Recommendations
    # ==========================

    story.append(
        Paragraph(
            "<font size=15 color='darkgreen'><b>Recommendations</b></font>",
            styles["Heading2"]
        )
    )

    if patient["prediction"] == 1:

        story.append(Paragraph("• Consult a healthcare professional immediately.", styles["BodyText"]))
        story.append(Paragraph("• Reduce sugar intake and avoid processed foods.", styles["BodyText"]))
        story.append(Paragraph("• Exercise at least 30 minutes daily.", styles["BodyText"]))
        story.append(Paragraph("• Monitor blood glucose regularly.", styles["BodyText"]))

    else:

        story.append(Paragraph("• Maintain your healthy lifestyle.", styles["BodyText"]))
        story.append(Paragraph("• Continue regular physical activity.", styles["BodyText"]))
        story.append(Paragraph("• Eat a balanced diet.", styles["BodyText"]))
        story.append(Paragraph("• Schedule routine health checkups.", styles["BodyText"]))

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    # ==========================
    # Disclaimer
    # ==========================

    story.append(
        Paragraph(
            "<font size=15 color='darkblue'><b>Medical Disclaimer</b></font>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report is generated using Machine Learning and Artificial Intelligence "
            "for educational and preliminary assessment purposes only. "
            "It is not a substitute for professional medical diagnosis or treatment. "
            "Please consult a qualified healthcare professional before making any medical decisions.",
            styles["BodyText"]
        )
    )

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    story.append(
    Paragraph(
        "<b>Authorized Signature</b>",
        styles["Heading2"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    # signature = Image("static/images/signature.png", width=120, height=60)
    # story.append(signature)

    story.append(
        Paragraph(
           "<b>Dr. AI MedCare</b><br/>AI Medical Diagnosis System",
           styles["Normal"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="AI_Medical_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)