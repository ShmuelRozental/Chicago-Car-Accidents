from ..connect import database


class AccidentRepository:
    def __init__(self):
        self.collection = database.get_collection('Accidents')

    def insert_accident_records(self, records):
        """Inserts accident records in bulk."""
        if records:
            self.collection.insert_many(records)

    def get_accidents_by_area_and_time(self, beat_of_occurrence, start_date=None, end_date=None):
        """Fetch accidents filtered by area and optional time range."""
        query = {"beat_of_occurrence": beat_of_occurrence}

        if start_date and end_date:
            query["crash_date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query["crash_date"] = {"$gte": start_date}
        elif end_date:
            query["crash_date"] = {"$lte": end_date}

        return list(self.collection.find(query)), 

    def get_accidents_grouped_by_cause(self, beat_of_occurrence):
        """Fetch accidents grouped by main cause, handling null values."""
        pipeline = [
            {
                "$match": {"beat_of_occurrence": beat_of_occurrence}
            },
            {
                "$group": {
                    "_id": {"$ifNull": ["$cause_id", "Unknown Cause"]},
                    "count": {"$sum": 1}
                }
            },
            {
                "$lookup": {
                    "from": "AccidentCauses",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "cause_details"
                }
            },
            {
                "$unwind": {
                    "path": "$cause_details",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "cause": {"$ifNull": ["$cause_details.cause_description", "Unknown Cause"]},
                    "count": 1,
                    "_id": 0
                }
            }
        ]
        results = database.get_collection('Accidents').aggregate(pipeline)
        return list(results)

    def get_injury_statistics(self, beat_of_occurrence):
        """Fetch injury statistics for a specific area, including injuries leading to death and non-fatal injuries."""
        pipeline = [
            {
                "$match": {
                    "beat_of_occurrence": beat_of_occurrence
                }
            },
            {
                "$unwind": "$injuries"
            },
            {
                "$group": {
                    "_id": None,  
                    "total_count": {"$sum": 1},
                    "fatal_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$injuries.fatal", True]},
                                1,
                                0
                            ]
                        }
                    },
                    "non_fatal_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$injuries.fatal", False]},
                                1,
                                0
                            ]
                        }
                    },
                    "events": {"$push": "$$ROOT"}
                }
            },
            {
                "$project": {
                    "total_count": 1,
                    "fatal_count": 1,
                    "non_fatal_count": 1,
                    "events": 1,
                    "_id": 0
                }
            }
        ]

        results = database.get_collection('Accidents').aggregate(pipeline)
        return list(results)

