import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from .data_utils import parse_date
from ..dal.connect import database
from ..dal.repositories.accident_repository import AccidentRepository

BATCH_SIZE = 1000
CHUNK_SIZE = 10000

def parse_injuries(row):
    """Parses injury data from CSV row."""
    try:
        return [
            {
                "type": injury_type,
                "severity": injury_severity,
                "fatal": is_fatal
            }
            for injury_type, injury_severity, is_fatal in zip(
                row.get('INJURY_TYPE', '').split(','),
                row.get('INJURY_SEVERITY', '').split(','),
                map(lambda x: x.strip().lower() == 'true', row.get('INJURY_FATAL', '').split(','))
            )
        ]
    except Exception as e:
        print(f"Error parsing injuries: {e}")
        return []

def drop_collection_if_exists(collection_name):
    """Drops a collection if it exists."""
    if collection_name in database.get_all_collection():
        database.drop_collection(collection_name)

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