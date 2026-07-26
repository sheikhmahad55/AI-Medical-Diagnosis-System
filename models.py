from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    glucose = db.Column(db.Float)
    bloodpressure = db.Column(db.Float)
    insulin = db.Column(db.Float)
    bmi = db.Column(db.Float)

    risk = db.Column(db.Integer)

    prediction = db.Column(db.Integer)
    prediction_text = db.Column(db.String(30))
    health = db.Column(db.String(50))