import csv
from typing import Dict, Any, List

def export_dict_to_csv(data: Dict[str, Any], filename: str):
    """
    Exports a dictionary to a CSV file. 
    If the dictionary contains lists of values, it will be exported as multiple rows.
    """
    if not data:
        return

    # Handle case where data is a single dict but values are lists (columnar format)
    # or a list of dicts (row format)
    
    if isinstance(data, dict):
        # Check if it's columnar data (values are lists of the same length)
        first_val = next(iter(data.values()))
        if isinstance(first_val, list):
            headers = data.keys()
            rows = zip(*data.values())
        else:
            # Single row
            headers = data.keys()
            rows = [data.values()]
    elif isinstance(data, list):
        # List of dicts
        headers = data[0].keys()
        rows = [d.values() for d in data]
    else:
        raise TypeError("Data must be a dictionary or a list of dictionaries")

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
