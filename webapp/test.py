import requests
from pprint import pprint

def fetch_data():
    response = requests.get('http://localhost:5000/api/data')
    response.raise_for_status()
    return response.json()

def add_record():
    response = requests.post(
        'http://localhost:5000/api/data', 
        json={"f1": 1, "f2": 2, "category": "A"}
    )
    response.raise_for_status()
    return response.json()

def remove_record(record_id):
    response = requests.delete(f'http://localhost:5000/api/data/{record_id}')
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print("\nInitial data:")
    data = fetch_data()
    pprint(data)
    print("length:", len(data))

    print("\nAdding records:")    
    pprint(add_record())
    pprint(add_record())
    pprint(add_record())
    
    print("\nData after additions:")
    data = fetch_data()
    pprint(data)
    print("length:", len(data))

    print("\nRemoving all records")
    for record in data:
        remove_record(record['id'])

    print("\nData after removals:")
    data = fetch_data()
    pprint(data)
    print("length:", len(data))