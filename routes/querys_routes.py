from ..services import AccidentService
from flask import Blueprint, request, jsonify
from ..utils.data_utils import serialize_data


queries_bp = Blueprint('queries', __name__)
accident_service = AccidentService()

@queries_bp.route('/accidents/area', methods=['GET'])
def accidents_by_area():
    beat_of_occurrence = request.args.get('beat_of_occurrence')

    if not beat_of_occurrence:
        return jsonify({"error": "Missing 'beat_of_occurrence' parameter"}), 400

    try:
        beat_of_occurrence = int(beat_of_occurrence)

        accidents, status_code = accident_service.fetch_accidents_by_area_and_time(beat_of_occurrence)

        if status_code == 404:
            return jsonify(accidents), 404

        serialized_accidents = serialize_data(accidents)
        return jsonify(serialized_accidents), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@queries_bp.route('/accidents/area-time', methods=['GET'])
def accidents_by_area_and_time():
    beat_of_occurrence = request.args.get('beat_of_occurrence')
    start_date = request.args.get('start_date')  # Optional
    end_date = request.args.get('end_date')      # Optional

    if not beat_of_occurrence:
        return jsonify({"error": "Missing 'beat_of_occurrence' parameter"}), 400

    try:
        beat_of_occurrence = int(beat_of_occurrence)

        accidents, status_code = accident_service.fetch_accidents_by_area_and_time(
            beat_of_occurrence, start_date, end_date
        )

        if status_code == 404:
            return jsonify(accidents), 404

        serialized_accidents = serialize_data(accidents)
        return jsonify(serialized_accidents), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@queries_bp.route('/accidents/grouped-by-cause', methods=['GET'])
def accidents_grouped_by_cause():
    beat_of_occurrence = request.args.get('beat_of_occurrence')

    if not beat_of_occurrence:
        return jsonify({"error": "Missing 'beat_of_occurrence' parameter"}), 400

    try:
        beat_of_occurrence = int(beat_of_occurrence)

        accidents, status_code = accident_service.fetch_accidents_grouped_by_cause(beat_of_occurrence)

        if status_code == 404:
            return jsonify(accidents), 404

        serialized_accidents = serialize_data(accidents)
        return jsonify(serialized_accidents), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@queries_bp.route('/accidents/injury-statistics', methods=['GET'])
def injury_statistics():
    beat_of_occurrence = request.args.get('beat_of_occurrence')

    if not beat_of_occurrence:
        return jsonify({"error": "Missing 'beat_of_occurrence' parameter"}), 400

    try:
        beat_of_occurrence = int(beat_of_occurrence)

        statistics, status_code = accident_service.fetch_injury_statistics(beat_of_occurrence)

        if status_code == 404:
            return jsonify(statistics), 404
        serialized_statistic = serialize_data(statistics)
        return jsonify(serialized_statistic), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
