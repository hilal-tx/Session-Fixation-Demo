1. Giriş ve Tanım

Session Fixation, bir saldırganın geçerli bir kullanıcı oturumunu (session) önceden belirleyerek kurbana dayatması ve kurban giriş yaptıktan sonra bu oturumu ele geçirmesi zafiyetidir. Bu saldırıda saldırgan şifre çalmaz; bunun yerine kurbana "önceden onaylanmış bir bilet" kullandırır.
2. Tehdit Modellemesi (Saldırı Senaryosu)

Projemizde simüle edilen saldırı adımları şöyledir:

    Hazırlık: Saldırgan, hedef siteden henüz giriş yapılmamış boş bir Session ID elde eder.

    Tuzak: Bu ID'yi bir URL parametresi veya cookie enjeksiyonu ile kurbana gönderir.

    Zafiyet: Kurban bu linke tıklar ve kendi hesabına giriş yapar. Uygulama, girişten sonra Session ID değerini yenilemezse, saldırganın elindeki ID artık "yetkili" hale gelir.

    Erişim: Saldırgan, elindeki ID ile tarayıcısından siteye girer ve kurbanın hesabına tam erişim sağlar.

3. Teknik Uygulama (Kod Analizi)

Hazırlanan laboratuvar ortamı Python Flask framework'ü ile iki farklı mantıkta kodlanmıştır:
A. Zafiyetli Mantık (/login_vulnerable)

Bu fonksiyonda, session['user'] ataması yapılırken mevcut oturum kimliği (_id) korunur. Flask'ın varsayılan davranışı, aksi belirtilmedikçe mevcut cookie'yi kullanmaya devam etmektir. Bu durum, saldırganın "Sabitlenmiş ID" ile içeride kalmasına neden olur.
B. Güvenli Mantık (/login_secure)

Güvenli modda iki kritik işlem yapılır:

    session.clear(): Mevcut tüm oturum verileri ve eski ID temizlenir.

    session.permanent = True: Flask'ın yeni bir güvenli oturum objesi ve benzersiz bir ID (UUID) üretmesi tetiklenir.

4. Uygulama Ekran Görüntüleri ve İspat

(Buraya projeyi çalıştırırken aldığın ekran görüntülerini eklemelisin)

    Görsel 1: Giriş yapmadan önceki Session ID durumu.

    Görsel 2: "Zafiyetli Giriş" sonrası ID'nin aynı kaldığının ispatı.

    Görsel 3: "Güvenli Giriş" sonrası ID'nin tamamen değiştiğinin (yenilendiğinin) ispatı.

5. Sonuç ve Öneriler

Yapılan simülasyon sonucunda, kullanıcıların kimlik doğrulama seviyesi değiştiği anda (Login/Logout) oturum kimliklerinin mutlaka yenilenmesi gerektiği kanıtlanmıştır. Web geliştiricilere önerilen en güvenli uygulama, her başarılı Login işleminde eski oturumu sonlandırıp (Destroy) kullanıcıya sunucu tarafından üretilen yeni bir token atanmasıdır.
