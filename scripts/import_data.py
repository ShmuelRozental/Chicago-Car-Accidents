import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from ..dal.connect import database
from ..dal.repositories.accident_repository import AccidentRepository
from ..utils.csv_utils import parse_date, parse_injuries, drop_collection_if_exists

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/Traffic_Crashes_-_Crashes - 20k rows')
BATCH_SIZE = 1000  
CHUNK_SIZE = 10000  

def get_or_insert(collection_name, data, cache):
    """Gets or inserts data into a collection and caches it."""
    key = data['device_name'] if 'device_name' in data else data['condition'] if 'condition' in data else data['cause_description']
    if key not in cache:
        collection = database.get_collection(collection_name)
        cache[key] = collection.insert_one(data).inserted_id
    return cache[key]

def prepare_accident_record(row, traffic_devices, weather_conditions, accident_causes):
    """Prepares a single accident record."""
    return {
        "crash_record_id": row.get('CRASH_RECORD_ID'),
        "crash_date": parse_date(row.get('CRASH_DATE')),
        "posted_speed_limit": row.get('POSTED_SPEED_LIMIT'),
        "traffic_control_device_id": traffic_devices.get(row.get('TRAFFIC_CONTROL_DEVICE')),
        "weather_condition_id": weather_conditions.get(row.get('WEATHER_CONDITION')),
        "lighting_condition": row.get('LIGHTING_CONDITION'),
        "cause_id": accident_causes.get(row.get('PRIM_CONTRIBUTORY_CAUSE')),
        "beat_of_occurrence": row.get('BEAT_OF_OCCURRENCE'),
        "location": {
            "type": "Point",
            "coordinates": [row.get('LONGITUDE'), row.get('LATITUDE')]
        },
        "injuries": parse_injuries(row)
    }

def process_chunk(chunk, traffic_devices, weather_conditions, accident_causes):
    """Processes a chunk of the CSV and returns accident records."""
    records = []
    for _, row in chunk.iterrows():
        record = prepare_accident_record(row, traffic_devices, weather_conditions, accident_causes)
        records.append(record)
    return records

def import_accident_data(csv_file_path):
    """Imports accident data into MongoDB with optimizations."""
    accident_repo = AccidentRepository()
    for collection in database.get_all_collection():
        drop_collection_if_exists(collection)

    traffic_devices, weather_conditions, accident_causes = {}, {}, {}

    # Batch processing traffic control devices, weather conditions, and accident causes
    with pd.read_csv(csv_file_path, chunksize=CHUNK_SIZE) as reader:
        for chunk in reader:
            for _, row in chunk.iterrows():
                # Traffic Control Devices
                device_name = row.get('TRAFFIC_CONTROL_DEVICE')
                if device_name and device_name not in traffic_devices:
                    device_data = {"device_name": device_name, "condition": row.get('DEVICE_CONDITION')}
                    traffic_devices[device_name] = get_or_insert('TrafficControlDevices', device_data, traffic_devices)

                # Weather Conditions
                condition_name = row.get('WEATHER_CONDITION')
                if condition_name and condition_name not in weather_conditions:
                    condition_data = {"condition": condition_name}
                    weather_conditions[condition_name] = get_or_insert('WeatherConditions', condition_data, weather_conditions)

                # Accident Causes
                cause_name = row.get('PRIM_CONTRIBUTORY_CAUSE')
                if cause_name and cause_name not in accident_causes:
                    cause_data = {"cause_description": cause_name}
                    accident_causes[cause_name] = get_or_insert('AccidentCauses', cause_data, accident_causes)

    # Insert accident records in batches
    accident_collection = database.get_collection('Accidents')
    accident_collection.drop_indexes()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for chunk in pd.read_csv(csv_file_path, chunksize=CHUNK_SIZE):
            future = executor.submit(
                process_chunk, chunk, traffic_devices, weather_conditions, accident_causes
            )
            futures.append(future)

        for future in futures:
            records = future.result()
            for i in range(0, len(records), BATCH_SIZE):
                accident_repo.insert_accident_records(records[i:i + BATCH_SIZE])

    accident_collection.create_index([("crash_record_id", 1)], unique=True)
    accident_collection.create_index([("crash_date", 1)])

    print("Data imported successfully!")

class AccidentRepository:
    def insert_accident_records(self, records):
        """Inserts multiple accident records using MongoDB's insert_many."""
        if records:
            database.get_collection('Accidents').insert_many(records)
