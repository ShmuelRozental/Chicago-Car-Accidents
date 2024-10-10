from datetime import datetime, timedelta
from bson import ObjectId

def get_total_accidents_by_area(database, area):
    return list(database.get_collection('AccidentRecords').aggregate([
        {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": area["coordinates"]},
                "distanceField": "dist.calculated",
                "maxDistance": area["maxDistance"],
                "query": {},
                "spherical": True
            }
        },
        {"$count": "total_accidents"}
    ]))

def get_total_accidents_by_area_and_period(database, area, start_date, end_date):
    return database.get_collection('AccidentRecords').count_documents({
        "location.coordinates": area["coordinates"],
        "crash_date": {"$gte": start_date, "$lt": end_date}
    })

def get_accidents_by_primary_cause(database, cause, area):
    return list(database.get_collection('AccidentRecords').aggregate([
        {
            "$match": {
                "cause_id": ObjectId(cause),
                "location.coordinates": area["coordinates"]
            }
        },
        {"$group": {"_id": "$cause_id", "total": {"$sum": 1}}}
    ]))

def get_injury_statistics(database, area):
    return list(database.get_collection('AccidentRecords').aggregate([
        {
            "$match": {
                "location.coordinates": area["coordinates"]
            }
        },
        {
            "$group": {
                "_id": None,
                "total_injuries": {"$sum": {"$size": "$injuries"}},
                "fatal_injuries": {"$sum": {
                    "$size": {
                        "$filter": {
                            "input": "$injuries",
                            "as": "injury",
                            "cond": {"$eq": ["$$injury.fatal", True]}
                        }
                    }
                }},
                "non_fatal_injuries": {"$sum": {
                    "$size": {
                        "$filter": {
                            "input": "$injuries",
                            "as": "injury",
                            "cond": {"$eq": ["$$injury.fatal", False]}
                        }
                    }
                }}
            }
        }
    ]))
