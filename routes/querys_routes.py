from flask import Flask, request, jsonify
from repository import get_total_accidents_by_area, get_total_accidents_by_area_and_period, get_accidents_by_primary_cause, get_injury_statistics
from dal.connect import database

app = Flask(__name__)

@app.route('/accidents/area', methods=['GET'])
def accidents_by_area():
    area = request.args.get('area')
    coordinates = [float(coord) for coord in request.args.get('coordinates').split(',')]
    area_data = {"coordinates": coordinates, "maxDistance": 1000}
    total_accidents = get_total_accidents_by_area(database, area_data)
    return jsonify(total_accidents)

@app.route('/accidents/area/period', methods=['GET'])
def accidents_by_area_and_period():
    area = request.args.get('area')
    coordinates = [float(coord) for coord in request.args.get('coordinates').split(',')]
    start_date = datetime.fromisoformat(request.args.get('start_date'))
    end_date = datetime.fromisoformat(request.args.get('end_date'))
    area_data = {"coordinates": coordinates}
    total_accidents = get_total_accidents_by_area_and_period(database, area_data, start_date, end_date)
    return jsonify({"total_accidents": total_accidents})

@app.route('/accidents/cause', methods=['GET'])
def accidents_by_primary_cause_route():
    cause = request.args.get('cause')
    area = request.args.get('area')
    coordinates = [float(coord) for coord in request.args.get('coordinates').split(',')]
    area_data = {"coordinates": coordinates}
    accidents = get_accidents_by_primary_cause(database, cause, area_data)
    return jsonify(accidents)

@app.route('/injuries/statistics', methods=['GET'])
def injury_statistics():
    area = request.args.get('area')
    coordinates = [float(coord) for coord in request.args.get('coordinates').split(',')]
    area_data = {"coordinates": coordinates}
    statistics = get_injury_statistics(database, area_data)
    return jsonify(statistics)

if __name__ == '__main__':
    app.run(debug=True)
