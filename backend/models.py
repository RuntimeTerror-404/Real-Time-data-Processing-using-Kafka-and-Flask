from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
