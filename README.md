# 🛡️ Session Fixation (Oturum Sabitleme) Vulnerability & Defense Lab

🇹🇷 **Türkçe**

📘 **Ders:** Güvenli Web Yazılımı Geliştirme 

🎯 **Görev:** Vize Projesi  

👤 **Hazırlayan:** Hilal Şengül 

# 🏫 İstinye Üniversitesi |

# 🛡️ Session Fixation Demo Lab
![Web Security](https://img.shields.io/badge/OWASP-A01-blue) ![Status](https://img.shields.io/badge/Status-Success-green)

## 📑 İçindekiler
* [Zafiyet Analizi](#zafiyet-analizi)
* [Güvenli Kodlama](#güvenli-kodlama)
* [Docker Kurulumu](#docker-kurulumu)

## 📖 Proje Özeti
Bu proje, **Güvenli Web Geliştirme** dersi kapsamında, oturum yönetimindeki en kritik zafiyetlerden biri olan **Session Fixation (Oturum Sabitleme)** saldırısını simüle etmek ve çözüm yollarını uygulamalı olarak göstermek amacıyla geliştirilmiştir. 

Proje, Python Flask framework'ü üzerinden canlı bir web arayüzü sunarak; giriş öncesi elde edilen bir oturum biletinin (Session ID), girişten sonra da geçerli kalmasının (Zafiyet) yarattığı riskleri ve bu ID'nin giriş anında yenilenmesinin (Savunma) önemini ispatlar.

---

## 🛠️ Teknik Altyapı
- **Dil:** Python 3.x
- **Framework:** Flask (Oturum yönetimi için `session` kütüphanesi)
- **Konsept:** Session ID Regeneration (Oturum Kimliği Yenileme)

---

## 💻 Uygulama Senaryoları

### 1. Senaryo: Zafiyetli Giriş (Session Fixation Mevcut)
Bu senaryoda uygulama, kullanıcının giriş yapmadan önceki oturum kimliğini kabul eder ve giriş yaptıktan sonra da aynı kimliği kullanmaya devam eder. 
* **Saldırı Vektörü:** Saldırgan, bildiği bir Session ID'yi kurbana "phishing" yoluyla kabul ettirirse, kurban giriş yaptığı an saldırgan da hesaba erişmiş olur.

### 2. Senaryo: Güvenli Giriş (Savunma Aktif)
Bu senaryoda uygulama, giriş yapıldığı an `session.clear()` ve oturum yenileme mantığını çalıştırır.
* **Sonuç:** Kullanıcı başarılı bir giriş yaptığı saniyede eski oturum kimliği imha edilir ve sunucu tarafından **tertemiz, yepyeni bir kimlik (ID)** atanır.

---

## 🚀 Kurulum ve Çalıştırma
Projenin yerel makinede çalıştırılması için:
1. Gerekli kütüphaneleri kurun: `pip install flask`
4. Uygulamayı başlatın: `python app.py`
5. Tarayıcıdan `http://127.0.0.1:5000` adresine giderek testleri gerçekleştirin.

---

## 🎥 Demo

Uygulamanın zafiyet ve çözüm adımlarını gösteren demo videosunu aşağıdaki lokasyondan izleyebilirsiniz:

./demo/project-demo.webm
