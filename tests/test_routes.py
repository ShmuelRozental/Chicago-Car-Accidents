import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_accidents_by_area(client):
    response = client.get('/accidents/area?area=test&coordinates=34.0,32.0')
    assert response.status_code == 200
    assert 'total_accidents' in response.get_json()

def test_accidents_by_area_and_period(client):
    response = client.get('/accidents/area/period?area=test&coordinates=34.0,32.0&start_date=2023-01-01&end_date=2023-01-31')
    assert response.status_code == 200

def test_accidents_by_primary_cause(client):
    response = client.get('/accidents/cause?cause=60d5f82f9f1b2c2f0e8b4567&area=test&coordinates=34.0,32.0')
    assert response.status_code == 200

def test_injury_statistics(client):
    response = client.get('/injuries/statistics?area=test&coordinates=34.0,32.0')
    assert response.status_code == 200
