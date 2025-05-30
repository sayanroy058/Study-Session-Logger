import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Study Session Logger' in response.data

def test_add_session(client):
    response = client.post('/add', data={
        'subject': 'History',
        'duration': '60',
        'notes': 'WWII research'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'History' in response.data

def test_add_invalid_session(client):
    response = client.post('/add', data={
        'subject': '',
        'duration': '30',
        'notes': 'No subject'
    }, follow_redirects=True)
    # Should still redirect, but not insert data
    assert response.status_code == 200
    assert b'No subject' not in response.data
