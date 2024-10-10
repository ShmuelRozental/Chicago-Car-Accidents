import os
import pandas as pd
from dal.connect import database

def import_accident_data(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)


        traffic_control_devices = []
        for _, row in df.iterrows():
            device_data = {
                "device_name": row.get('TRAFFIC_CONTROL_DEVICE'),
                "condition": row.get('DEVICE_CONDITION')
            }
            device_id = database.get_collection('TrafficControlDevices').insert_one(device_data).inserted_id
            traffic_control_devices.append(device_id)

        weather_conditions = []
        for _, row in df.iterrows():
            condition_data = {
                "condition": row.get('WEATHER_CONDITION')
            }
            condition_id = database.get_collection('WeatherConditions').insert_one(condition_data).inserted_id
            weather_conditions.append(condition_id)

        accident_causes = []
        for _, row in df.iterrows():
            cause_data = {
                "cause_description": row.get('PRIM_CONTRIBUTORY_CAUSE')
            }
            cause_id = database.get_collection('AccidentCauses').insert_one(cause_data).inserted_id
            accident_causes.append(cause_id)

        accident_records = []
        for i, row in df.iterrows():
            accident_data = {
                "crash_record_id": row.get('CRASH_RECORD_ID'),
                "crash_date": pd.to_datetime(row.get('CRASH_DATE')),
                "posted_speed_limit": row.get('POSTED_SPEED_LIMIT'),
                "traffic_control_device_id": traffic_control_devices[i],
                "weather_condition_id": weather_conditions[i],
                "lighting_condition": row.get('LIGHTING_CONDITION'),
                "cause_id": accident_causes[i],
                "location": {
                    "type": "Point",
                    "coordinates": [row.get('LONGITUDE'), row.get('LATITUDE')]
                },
                "injuries": [
                    {"type": injury_type, "severity": injury_severity, "fatal": is_fatal}
                    for injury_type, injury_severity, is_fatal in zip(
                        row.get('INJURY_TYPE', '').split(','),
                        row.get('INJURY_SEVERITY', '').split(','),
                        map(lambda x: x.strip().lower() == 'true', row.get('INJURY_FATAL', '').split(','))
                    )
                ]
            }
            accident_records.append(accident_data)


        database.get_collection('AccidentRecords').insert_many(accident_records)

        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error importing data: {e}")

