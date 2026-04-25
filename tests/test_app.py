import pytest
import sys
import os

# src klasöründeki app.py modülüne erişmek için yolu ayarlayalım
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Ana sayfanın başarıyla yüklendiğini test et"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Session Fixation" in response.data

def test_login_vulnerable(client):
    """Zafiyetli girişin eski oturum verilerini KORUDUĞUNU test et"""
    # Önceden oturumda var olan sahte veri
    with client.session_transaction() as sess:
        sess['eski_veri'] = 'hacker_tarafindan_bilinen_deger'
    
    # Zafiyetli girişe istek at
    response = client.post('/login_vulnerable', follow_redirects=True)
    assert response.status_code == 200
    
    with client.session_transaction() as sess:
        assert sess['user'] == 'Kurban_Hesabi'
        # Zafiyet: Eski oturum verisi silinmediği için Session Fixation oluşur
        assert 'eski_veri' in sess
        assert sess['eski_veri'] == 'hacker_tarafindan_bilinen_deger'

def test_login_secure(client):
    """Güvenli girişin eski oturum verilerini TEMİZLEDİĞİNİ test et"""
    # Önceden oturumda var olan sahte veri
    with client.session_transaction() as sess:
        sess['eski_veri'] = 'hacker_tarafindan_bilinen_deger'
        
    # Güvenli girişe istek at
    response = client.post('/login_secure', follow_redirects=True)
    assert response.status_code == 200
    
    with client.session_transaction() as sess:
        assert sess['user'] == 'Güvenli_Hesap'
        # Güvenlik: Eski veriler silindiği için eski session id geçersizleşir / sıfırlanır
        assert 'eski_veri' not in sess
        assert sess.permanent == True

def test_logout(client):
    """Çıkış işleminin oturumu başarıyla temizlediğini test et"""
    with client.session_transaction() as sess:
        sess['user'] = 'test_user'
        
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert 'user' not in sess
