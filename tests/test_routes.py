import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_home(client):
    response = client.get('/')
    assert b"Welcome to the Advanced Flask App!" in response.data

def test_register(client):
    response = client.post('/register', data=dict(
        username='testuser',
        password='testpassword',
        confirm_password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    assert user is not None

def test_login(client):
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword',
        confirm_password='testpassword'
    ), follow_redirects=True)
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the Advanced Flask App!" in response.data
