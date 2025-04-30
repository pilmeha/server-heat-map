from flask import jsonify, request, render_template
from app import db, app
from app.models import Sensor


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')

@app.route('/sensors')
def sensors():
    all_sensors = Sensor.query.all()
    return render_template('sensors.html', sensors=all_sensors)

@app.route('/api/data', methods=['GET', 'POST'])
def sensor_data():
    if request.method == 'POST':
        data = request.get_json()
        new_data = Sensor(
            sensor_id=data['sensor_id'],
            temperature=data['temperature'],
            humidity=data.get('humidity'),
            x_coord=data['x'],
            y_coord=data['y']
        )
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'message': 'Data recorded'}), 201
    
    data = Sensor.query.order_by(Sensor.timestamp.desc()).limit(50).all()
    return jsonify([{
        'sensor_id': item.sensor_id,
        'temperature': item.temperature,
        'x': item.x_coord,
        'y': item.y_coord,
        'timestamp': item.timestamp.isoformat()
    } for item in data])