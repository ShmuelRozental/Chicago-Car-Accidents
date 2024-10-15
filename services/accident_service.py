from  ..dal.repositories import AccidentRepository
from datetime import datetime

class AccidentService:
    def __init__(self):
        self.accident_repo = AccidentRepository()

    def fetch_accidents_by_area_and_time(self, beat_of_occurrence, start_date=None, end_date=None):
        """Fetch accidents by area and optional time range."""
        if not isinstance(beat_of_occurrence, int):
            raise ValueError("'beat_of_occurrence' must be an integer")

      
        start_date = self._parse_date(start_date)
        end_date = self._parse_date(end_date)

        accidents = self.accident_repo.get_accidents_by_area_and_time(
            beat_of_occurrence, start_date, end_date
        )

        if not accidents:
            return {"message": "No accidents found for the given area and time range."}, 404

        return accidents, 200

    def fetch_accidents_grouped_by_cause(self, beat_of_occurrence):
        """Fetch and group accidents by the main cause."""
        if not isinstance(beat_of_occurrence, int):
            raise ValueError("'beat_of_occurrence' must be an integer")

        accidents = self.accident_repo.get_accidents_grouped_by_cause(beat_of_occurrence)

        if not accidents:
            return {"message": "No accidents found for the given area."}, 404

        return accidents, 200
    

    def fetch_injury_statistics(self, beat_of_occurrence):
        """Fetch injury statistics for a specific area."""
        if not isinstance(beat_of_occurrence, int):
            raise ValueError("beat_of_occurrence must be an integer.")

        statistics = self.accident_repo.get_injury_statistics(beat_of_occurrence)

        if not statistics:
            return [], 404

        return statistics, 200


    def _parse_date(self, date_str):
        """Helper function to parse date strings."""
        if date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date format: '{date_str}'. Use 'YYYY-MM-DD'.")
        return None
