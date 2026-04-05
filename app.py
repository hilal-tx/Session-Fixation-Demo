from flask import Flask, session, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Güvenli oturum imzası için

# Web arayüzü (HTML)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Session Fixation Test Lab</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 50px; background-color: #f0f2f5; color: #333; }
        .container { max-width: 700px; margin: auto; border: 1px solid #ddd; padding: 30px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .session-info { background: #eef2ff; border-left: 5px solid #4f46e5; padding: 15px; margin-bottom: 25px; word-break: break-all; }
        .danger-btn { background: #dc2626; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; margin-bottom: 10px; }
        .success-btn { background: #16a34a; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }
        .logout-link { color: #666; text-decoration: none; display: block; margin-top: 20px; text-align: center; }
        code { font-weight: bold; color: #4f46e5; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🛡️ Session Fixation Savunma Laboratuvarı</h2>
        <div class="session-info">
            <strong>Mevcut Oturum ID (Session ID):</strong><br>
            <code>{{ session_id }}</code>
        </div>
        
        {% if 'user' in session %}
            <h3 style="color: #16a34a;">✅ Sisteme Giriş Yapıldı: {{ session['user'] }}</h3>
            <p>Oturum şu an aktif durumda. Hacker bu ID'yi önceden biliyorsa içeri sızabilir!</p>
            <a href="/logout" class="logout-link">Oturumu Kapat</a>
        {% else %}
            <h3>Giriş Yapmayı Deneyin:</h3>
            <form action="/login_vulnerable" method="post">
                <button type="submit" class="danger-btn">1. ZAFİYETLİ GİRİŞ (ID Sabit Kalır)</button>
            </form>
            <form action="/login_secure" method="post">
                <button type="submit" class="success-btn">2. GÜVENLİ GİRİŞ (ID Yenilenir)</button>
            </form>
            <p><small><i>Not: Bu laboratuvarda şifre kontrolü sembolik olarak pas geçilmiştir.</i></small></p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Flask session ID'sini kullanıcıya gösterir
    sid = session.get('_id', 'Henüz Oluşturulmadı')
    return render_template_string(HTML_TEMPLATE, session_id=sid)

@app.route('/login_vulnerable', methods=['POST'])
def login_vulnerable():
    # ZAFİYETLİ GİRİŞ: Oturum kimliği değiştirilmez.
    session['user'] = 'Kurban_Hesabi'
    return redirect(url_for('index'))

@app.route('/login_secure', methods=['POST'])
def login_secure():
    # GÜVENLİ GİRİŞ: Eski oturum verileri temizlenir ve yeni ID atanır.
    session.clear()
    session['user'] = 'Güvenli_Hesap'
    # session.permanent tetiklendiğinde veya veri değiştiğinde Flask yeni ID atar
    session.permanent = True 
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
