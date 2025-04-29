from flask import Flask, request, jsonify
from models import db, SensorData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.../database/sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Создание таблиц через CLI команду
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database tables created.')

# Прием данных
@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        new_entry = SensorData(
            sensor_id=data['sensor_id'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            x=data['x'],
            y=data['y']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data received"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error receiving data"}), 500

# Выдача последних данных
@app.route('/api/data', methods=['GET'])
def get_data():
    all_data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(50).all()
    result = []
    for entry in all_data:
        result.append({
            "sensor_id": entry.sensor_id,
            "temperature": entry.temperature,
            # "humidity": entry.humidity,
            "x": entry.x,
            "y": entry.y,
            "timestamp": entry.timestamp.isoformat()
        })
    # return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
