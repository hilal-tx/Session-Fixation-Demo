import pytest
import sys
import os

# Add the src directory to the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test if the index page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Session Fixation" in response.data

def test_login_vulnerable(client):
    """Test that vulnerable login RETAINS old session data"""
    # Pre-existing fake data in session
    with client.session_transaction() as sess:
        sess['old_data'] = 'value_known_by_hacker'
    
    # Request the vulnerable login endpoint
    response = client.post('/login_vulnerable', follow_redirects=True)
    assert response.status_code == 200
    
    with client.session_transaction() as sess:
        assert sess['user'] == 'Kurban_Hesabi'
        # Vulnerability: Old session data is not deleted, causing Session Fixation
        assert 'old_data' in sess
        assert sess['old_data'] == 'value_known_by_hacker'

def test_login_secure(client):
    """Test that secure login CLEARS old session data"""
    # Pre-existing fake data in session
    with client.session_transaction() as sess:
        sess['old_data'] = 'value_known_by_hacker'
        
    # Request the secure login endpoint
    response = client.post('/login_secure', follow_redirects=True)
    assert response.status_code == 200
    
    with client.session_transaction() as sess:
        assert sess['user'] == 'G\xc3\xbcvenli_Hesap' or sess['user'] == 'Güvenli_Hesap'
        # Security: Old data is deleted so the old session ID is invalidated / reset
        assert 'old_data' not in sess
        assert sess.permanent == True

def test_logout(client):
    """Test that the logout process clears the session successfully"""
    with client.session_transaction() as sess:
        sess['user'] = 'test_user'
        
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert 'user' not in sess
