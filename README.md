🛡️ Session Fixation (Oturum Sabitleme) Vulnerability Lab

🇹🇷 **Türkçe** 

## 📖 Proje Özeti
Bu proje, modern web uygulamalarında oturum yönetiminin (session management) kritik bir parçası olan **"Session Fixation (Oturum Sabitleme)"** zafiyetini ve çözümünü uygulamalı olarak göstermek için geliştirilmiş bir Python Flask laboratuvarıdır. 

Sistem, bir saldırganın kurbana "önceden tanımlanmış" bir Session ID'yi nasıl kabul ettirebileceğini (Zafiyetli Senaryo) ve bu zafiyetin her başarılı girişte `session.clear()` ve `session.permanent = True` mantığıyla oturum kimliğinin yenilenerek (Güvenli Senaryo) nasıl kesin olarak engellendiğini kanıtlar.

---

## 💻 Çekirdek Kod Mimarisi (Core Implementation)

Flask uygulamamızın içindeki zafiyetli ve güvenli giriş mekanizmalarının karşılaştırmalı kod analizi:

### 1. Zafiyetli Giriş (Vulnerable Login)
Bu fonksiyonda, kullanıcı giriş yaptıktan sonra sistem mevcut Session ID'yi değiştirmeden sadece kullanıcı bilgisini ekler.
```python
@app.route('/login_vulnerable', methods=['POST'])
def login_vulnerable():
    # ZAFİYETLİ GİRİŞ: Session ID olduğu gibi kalır, sadece kullanıcı bilgisi eklenir.
    # Saldırgan eski ID'yi bilirse kurbanın hesabına erişebilir.
    session['user'] = 'Kurban_Kullanici'
    return redirect(url_for('index'))

@app.route('/login_secure', methods=['POST'])
def login_secure():
    # GÜVENLİ GİRİŞ: Giriş yapıldığı an eski session temizlenir ve yeni ID verilir.
    session.clear() # Eski verileri siler
    session.permanent = True # Yeni bir session objesi oluşturulmasını tetikler
    session['user'] = 'Guvenli_Kullanici'
    return redirect(url_for('index'))
**

Bunu da yaptıktan sonra GitHub sayfasının altından **"Commit changes"** butonuna bas. GitHub tarafı bitti, efsanevi bir repo oldu!

---

### ADIM 2: Hocanın QLine Portalına Yazılacaklar (100 Puanlık Kısım)

Hocanın sitesindeki o kutucuklara da şu teknik metinleri kopyalayıp yapıştır:

**1. GITHUB DEPOSU Kutusuna:**
👉 `https://github.com/hilal-tx/session-fixation-demo` (Kendi repo linkini yapıştır).

**2. ÖZET / AMAÇ Kutusuna:**
> Bu proje, web uygulamalarında oturum kimliklerinin (Session ID) güvenli yönetimiyle ilgili kritik bir zafiyet olan "Session Fixation (Oturum Sabitleme)" konusunu uygulamalı olarak göstermeyi amaçlamaktadır. Proje, Python Flask üzerinde çalışan canlı bir laboratuvar sunarak, bir kullanıcının kimliği doğrulandıktan sonra bile saldırganın önceden bildiği oturum kimliğini kullanmaya devam etmesinin yarattığı riski (Zafiyet) ve bu riskin her başarılı girişte oturum kimliğinin kriptografik olarak yenilenmesiyle (Savunma) nasıl kesin olarak engellendiğini kanıtlar.

**3. MARKDOWN NOTLARI EKLE Kutusuna (Teknik Rapor):**
Aşağıdaki blokta yer alan metni kopyala ve o büyük kutuya yapıştır:

***

```markdown
# 🛡️ Teknik Uygulama ve Oturum Yönetimi Raporu

## 1. Teknik Altyapı
Proje, hafif ve esnek bir Python Web Framework olan **Flask** kullanılarak geliştirilmiştir. Uygulama, istemci tarafı (client-side) imzalı oturumları (sessions) simüle etmektedir. Sunucu, her oturum için benzersiz, kriptografik olarak güvenli bir `_id` atar ve bu ID tarayıcıda bir cookie olarak saklanır.

## 2. Zafiyet Analizi (Session Fixation Scenario)
Laboratuvarın zafiyetli senaryosunda, `/login_vulnerable` rotası kullanılmaktadır. Bu rota, kullanıcı başarılı bir şekilde giriş yapsa bile, mevcut Session ID'yi yenilememektedir.
* **Risk:** Bir saldırgan, kurbana önceden bildiği bir Session ID içeren bir link (örneğin phishing ile) veya cookie yerleştirirse ve kurban bu durumdayken giriş yaparsa, saldırgan da aynı Session ID'ye sahip olduğu için kurbanın oturumuna şifre bilmeden erişebilir.

## 3. Savunma Mekanizması (Session ID Regeneration)
Savunma senaryosunda, `/login_secure` rotası kullanılmaktadır. Bu rota, OWASP (Open Web Application Security Project) standartlarına uygun olarak tasarlanmıştır.
* **Mekanizma:** Kullanıcının kimliği doğrulandığı an, Flask'ın `session.clear()` fonksiyonu kullanılarak eski (kimliği doğrulanmamış) oturum tamamen iptal edilir. Ardından, `session.permanent = True` veya yeni verilerin eklenmesiyle, sunucu tarafından **kriptografik olarak güvenli, tertemiz ve yepyeni** bir Session ID üretilir.
* **Sonuç:** Saldırganın bildiği eski Session ID artık geçersizdir ve kurbanın hesabı güvendedir.

## 4. Simülasyon Sonuçları ve Doğrulama
Yapılan testlerde, zafiyetli giriş yönteminde Session ID'nin (UUID formatında) giriş öncesi ve sonrası tamamen aynı kaldığı; güvenli giriş yönteminde ise giriş yapıldığı an UUID'nin tamamen değiştiği gözlemlenmiştir. Bu, savunma mekanizmasının Session Fixation saldırı vektörünü kesin olarak engellediğini kanıtlamaktadır.
