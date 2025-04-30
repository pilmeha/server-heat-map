from datetime import datetime
from app import db

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float)
    x = db.Column(db.Float)  # Координата X на карте
    y = db.Column(db.Float)  # Координата Y
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"""<Sensor: 
            sensor_id: {self.sensor_id}
            temperatur: {self.temperature}
            humidity: {self.humidity}
            x: {self.x}
            y: {self.y}
            timestamp: {self.timestamp}
        """