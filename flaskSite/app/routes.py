from flask import jsonify, request, render_template
import plotly
import plotly.express as px
import pandas as pd
import sqlalchemy
from app import db, app
from app.models import Sensor

@app.route('/')
@app.route('/clever')
def clever():
    sensors = Sensor.query.all()
    return render_template('clever.html', sensors=sensors)

# @app.route('/api/chart-data/<sensor_id>')
# def chart_data(sensor_id):
#     query = sqlalchemy.text("""
#         SELECT timestamp, temperature
#         FROM sensor
#         WHERE sensor_id = :sensor_id
#         ORDER BY timestamp
#     """)
#     df = pd.read_sql(query, db.engine, params={"sensor_id": sensor_id})
#     fig = px.line(df, x='timestamp', y='temperature', title=f'Температура ({sensor_id})')
#     return jsonify(fig.to_dict())

@app.route('/dashboard')
def dashboard():
    # sensors = db.session.query(Sensor.sensor_id).distinct().all()
    # sensor_ids = [s[0] for s in sensors]
    # return render_template('dashboard.html', sensor_ids=sensor_ids)

    # Загружаем данные из БД
    queryTemp1 = """
        SELECT timestamp, temperature
        FROM sensor
        WHERE sensor_id = 'eltex-1'
        ORDER BY timestamp
    """
    dfT1 = pd.read_sql(queryTemp1, db.engine)
    figT1 = px.line(dfT1, x='timestamp', y='temperature', title='Температура (eltex-1)')
    plotT1 = figT1.to_html(full_html=False)

    queryHumi1 = """
        SELECT timestamp, humidity
        FROM sensor
        WHERE sensor_id = 'eltex-1'
        ORDER BY timestamp
    """
    dfH1 = pd.read_sql(queryHumi1, db.engine)
    figH1 = px.line(dfH1, x='timestamp', y='humidity', title='Влажность (eltex-1)')
    plotH1 = figH1.to_html(full_html=False)

    queryTemp2 = """
        SELECT timestamp, temperature
        FROM sensor
        WHERE sensor_id = 'eltex-2'
        ORDER BY timestamp
    """
    dfT2 = pd.read_sql(queryTemp1, db.engine)
    figT2 = px.line(dfT2, x='timestamp', y='temperature', title='Температура (eltex-2)')
    plotT2 = figT2.to_html(full_html=False)

    queryHumi2 = """
        SELECT timestamp, humidity
        FROM sensor
        WHERE sensor_id = 'eltex-2'
        ORDER BY timestamp
    """
    dfH2 = pd.read_sql(queryHumi1, db.engine)
    figH2 = px.line(dfH2, x='timestamp', y='humidity', title='Влажность (eltex-2)')
    plotH2 = figH2.to_html(full_html=False)


    queryTemp3 = """
        SELECT timestamp, temperature
        FROM sensor
        WHERE sensor_id = 'eltex-3'
        ORDER BY timestamp
    """
    dfT3 = pd.read_sql(queryTemp1, db.engine)
    figT3 = px.line(dfT3, x='timestamp', y='temperature', title='Температура (eltex-3)')
    plotT3 = figT3.to_html(full_html=False)

    queryHumi3 = """
        SELECT timestamp, humidity
        FROM sensor
        WHERE sensor_id = 'eltex-3'
        ORDER BY timestamp
    """
    dfH3 = pd.read_sql(queryHumi1, db.engine)
    figH3 = px.line(dfH3, x='timestamp', y='humidity', title='Влажность (eltex-3)')
    plotH3 = figH3.to_html(full_html=False)


    queryTemp4 = """
        SELECT timestamp, temperature
        FROM sensor
        WHERE sensor_id = 'eltex-4'
        ORDER BY timestamp
    """
    dfT4 = pd.read_sql(queryTemp1, db.engine)
    figT4 = px.line(dfT4, x='timestamp', y='temperature', title='Температура (eltex-4)')
    plotT4 = figT4.to_html(full_html=False)

    queryHumi4 = """
        SELECT timestamp, humidity
        FROM sensor
        WHERE sensor_id = 'eltex-4'
        ORDER BY timestamp
    """
    dfH4 = pd.read_sql(queryHumi1, db.engine)
    figH4 = px.line(dfH4, x='timestamp', y='humidity', title='Влажность (eltex-4)')
    plotH4 = figH4.to_html(full_html=False)

    # Преобразуем и строим график    
    return render_template('dashboard.html', plotT1=plotT1, plotH1=plotH1, plotT2=plotT2, plotH2=plotH2, plotT3=plotT3, plotH3=plotH3, plotT4=plotT4, plotH4=plotH4)

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
