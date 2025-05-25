from flask import jsonify, request, render_template
from app import db, app
from app.models import Sensor


@app.route('/')
def dome():
    return render_template('dome.html')

@app.route('/heatmap')
def heatmap():
    sensors = Sensor.query.all()
    return render_template('heatmap.html', sensors=sensors)

@app.route('/sensors')
def sensors():
    # написать запрос, который будет показывать только униальыне датчики
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
            x=data['x'],
            y=data['y']
        )
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'message': 'Data recorded'}), 201
    
    data = Sensor.query.order_by(Sensor.timestamp.desc()).limit(50).all()
    return jsonify([{
        'sensor_id': item.sensor_id,
        'temperature': item.temperature,
        'x': item.x,
        'y': item.y,
        'timestamp': item.timestamp.isoformat()
    } for item in data])
