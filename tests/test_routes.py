import json

def test_accidents_by_area(client, mocker):
    mocker.patch('services.accident_service.AccidentService.fetch_accidents_by_area_and_time',
                 return_value=([{"id": 424, "location": "Test Area"}], 200))

    response = client.get('/accidents/area?beat_of_occurrence=424')
    assert response.status_code == 200
    actual_data = json.loads(response.data)
    assert json.loads(actual_data) == [{"id": 424, "location": "Test Area"}]

def test_accidents_by_area_missing_param(client):
    response = client.get('/accidents/area')
    assert response.status_code == 400
    assert response.json == {"error": "Missing 'beat_of_occurrence' parameter"}

def test_accidents_by_area_and_time(client, mocker):
    mocker.patch('services.accident_service.AccidentService.fetch_accidents_by_area_and_time',
                 return_value=([{"id": 2, "location": "Area 2"}], 200))

    response = client.get('/accidents/area-time?beat_of_occurrence=1&start_date=2024-01-01&end_date=2024-12-31')
    assert response.status_code == 200
    actual_data = json.loads(response.data)
    assert json.loads(actual_data) == [{"id": 2, "location": "Area 2"}]

def test_accidents_grouped_by_cause(client, mocker):
    mocker.patch('services.accident_service.AccidentService.fetch_accidents_grouped_by_cause',
                 return_value=([{"cause": "Speeding", "count": 10}], 200))

    response = client.get('/accidents/grouped-by-cause?beat_of_occurrence=1')
    assert response.status_code == 200
    actual_data = json.loads(response.data)
    assert json.loads(actual_data) == [{"cause": "Speeding", "count": 10}]

def test_injury_statistics(client, mocker):
    mocker.patch('services.accident_service.AccidentService.fetch_injury_statistics',
                 return_value=({"fatal_count": 2, "non_fatal_count": 5}, 200))

    response = client.get('/accidents/injury-statistics?beat_of_occurrence=1')
    assert response.status_code == 200
    actual_data = json.loads(response.data)
    assert json.loads(actual_data) == {"fatal_count": 2, "non_fatal_count": 5}
