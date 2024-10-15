from datetime import datetime
from typing import Optional

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parses date string into a datetime object with flexible formats."""
    if date_str is None:
        return None  

    date_formats = [
        '%m/%d/%Y %I:%M %p',  
        '%m/%d/%Y %I:%M:%S %p',  
        '%m/%d/%Y %H:%M',      
        '%m/%d/%Y %H:%M:%S',   
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Error parsing date: '{date_str}'. Tried formats: {date_formats}")

from bson.json_util import dumps

def serialize_data(data):
    """Serialize MongoDB data to JSON format with indentation."""
    return dumps(data, indent=2)
