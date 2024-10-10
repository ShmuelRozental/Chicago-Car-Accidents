import os
from flask import Blueprint, request, jsonify
from import_data import import_accident_data

accident_bp = Blueprint('accidents', __name__)
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/Traffic_Crashes_-_Crashes - 20k rows.csv')

@accident_bp.route('/init', methods=['POST'])
def init_data():
    try:
        import_accident_data(CSV_FILE_PATH)
        return jsonify({"message": "Data initialized successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
