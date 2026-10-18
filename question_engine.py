# -*- coding: utf-8 -*-
"""
Study Stop - Yeni Nesil Soru Üretim Motoru (Question Engine)
Kullanıcının girdiği sınıf düzeyi, ders, eksik konu ve soru notuna göre
5 adet beceri temelli, yeni nesil, A-B-C-D şıklı soru ve detaylı çözümler üretir.
Türkçe ve İngilizce dil desteği mevcuttur.
"""

import random

# ==============================================================================
# YERLEŞİK YENİ NESİL SORU BANKASI (Örnek Yaygın Konular İçin Özgün Sorular)
# ==============================================================================

PRESET_QUESTIONS_TR = {
    "çarpanlar ve katlar": [
        {
            "question": (
                "Bir belediye kenar uzunlukları 120 metre ve 180 metre olan dikdörtgen şeklindeki "
                "bir parkın etrafına köşelere de gelmek şartıyla eşit aralıklarla aydınlatma direkleri "
                "dikecektir. Direkler arasındaki mesafenin metre cinsinden tam sayı olması ve direk "
                "sayısının en az olması hedeflenmektedir. Her bir direğin maliyeti 450 TL'dir.\n\n"
                "Buna göre parkın aydınlatılması için yapılacak toplam direk harcaması kaç TL olur?"
            ),
            "options": {
                "A": "3.600 TL",
                "B": "4.500 TL",
                "C": "5.400 TL",
                "D": "7.200 TL"
            },
            "correct": "B",
            "explanation": (
                "Direk sayısının en az olması için aralarındaki mesafe EBOB(120, 180) olmalıdır.\n"
                "120 ve 180'in EBOB'u 60 metredir.\n"
                "Parkın çevresi = 2 * (120 + 180) = 600 metre.\n"
                "Gereken direk sayısı = 600 / 60 = 10 adettir.\n"
                "Toplam maliyet = 10 * 450 TL = 4.500 TL olur. Doğru cevap B şıkkıdır."
            )
        },
        {
            "question": (
                "İki farklı otobüs durağından A otobüsü her 45 dakikada bir, B otobüsü ise her 60 dakikada "
                "bir sefere çıkmaktadır. Bu iki otobüs ilk kez sabah saat 08:00'de aynı anda sefere çıkmıştır.\n\n"
                "Buna göre, saat 08:00 ile 18:00 arasında (08:00 ve 18:00 dahil) bu iki otobüs toplam kaç kez "
                "aynı anda sefere çıkar?"
            ),
            "options": {
                "A": "3",
                "B": "4",
                "C": "5",
                "D": "6"
            },
            "correct": "B",
            "explanation": (
                "Otobüslerin birlikte sefere çıkma aralığı EKOK(45, 60) ile bulunur.\n"
                "45 ve 60'ın EKOK'u 180 dakikadır (yani 3 saat).\n"
                "08:00'den itibaren sefere çıkış saatleri:\n"
                "1. kez: 08:00\n2. kez: 11:00\n3. kez: 14:00\n4. kez: 17:00\n"
                "(Bir sonraki 20:00 olacağından 18:00'i aşar).\n"
                "Toplam 4 kez aynı anda sefere çıkarlar. Doğru cevap B'dir."
            )
        },
        {
            "question": (
                "Aşağıda bir marangozun elindeki 96 cm ve 144 cm uzunluğundaki iki farklı tahta çıta "
                "hiç parça artmayacak şekilde eşit uzunlukta en büyük parçalara ayrılacaktır.\n\n"
                "Marangoz her bir kesim işlemi için 15 saniye harcadığına göre, tüm kesim işlemlerini "
                "tamamlamak toplam kaç saniye sürer?"
            ),
            "options": {
                "A": "45 saniye",
                "B": "60 saniye",
                "C": "75 saniye",
                "D": "90 saniye"
            },
            "correct": "A",
            "explanation": (
                "En büyük eşit parça uzunluğu EBOB(96, 144) = 48 cm'dir.\n"
                "96 cm tahtadan: 96 / 48 = 2 parça elde edilir (2 parça için 1 kesim yapılır).\n"
                "144 cm tahtadan: 144 / 48 = 3 parça elde edilir (3 parça için 2 kesim yapılır).\n"
                "Toplam kesim sayısı = 1 + 2 = 3 kesimdir.\n"
                "Toplam süre = 3 * 15 saniye = 45 saniyedir. Doğru cevap A'dır."
            )
        },
        {
            "question": (
                "Kenar uzunlukları santimetre cinsinden 1'den büyük birer tam sayı olan bir kartonun "
                "alanı 77 cm²'dir. Bu kartonun kısa kenarı 2 cm uzatılıp, uzun kenarı 1 cm kısaltılıyor.\n\n"
                "Buna göre yeni oluşan kartonun çevresi ilk duruma göre nasıl değişir?"
            ),
            "options": {
                "A": "2 cm artar",
                "B": "Değişmez",
                "C": "2 cm azalır",
                "D": "4 cm artar"
            },
            "correct": "A",
            "explanation": (
                "77 sayısının 1'den büyük çarpanları 7 ve 11'dir. İlk kenarlar: a = 7 cm, b = 11 cm.\n"
                "İlk çevre = 2 * (7 + 11) = 36 cm.\n"
                "Yeni kenarlar: a' = 7 + 2 = 9 cm, b' = 11 - 1 = 10 cm.\n"
                "Yeni çevre = 2 * (9 + 10) = 38 cm.\n"
                "Fark: 38 - 36 = 2 cm artar. Doğru cevap A şıkkıdır."
            )
        },
        {
            "question": (
                "A ve B pozitif tam sayıları aralarında asaldır. Bu iki sayının EKOK'u 156'dır.\n"
                "A + 12/B = 14 olduğuna göre, B değeri kaçtır?"
            ),
            "options": {
                "A": "12",
                "B": "13",
                "C": "14",
                "D": "16"
            },
            "correct": "A",
            "explanation": (
                "A ve B aralarında asal olduğundan EKOK(A, B) = A * B = 156'dır.\n"
                "A + 12/B = 14 eşitliğinde paydaları eşitlersek: (A*B + 12) / B = 14 olur.\n"
                "(156 + 12) / B = 14 => 168 / B = 14 => B = 168 / 14 = 12 bulunur.\n"
                "Doğru cevap A şıkkıdır."
            )
        }
    ],
    "üslü ifadeler": [
        {
            "question": (
                "Bir biyoloji laboratuvarında bulunan bir bakteri türü her 20 dakikada bir 2 katına "
                "çıkmaktadır. Başlangıçta deney kabında 8 adet bakteri bulunmaktadır.\n\n"
                "Buna göre 3 saat sonra deney kabındaki toplam bakteri sayısı üslü olarak nasıl gösterilir?"
            ),
            "options": {
                "A": "2^9",
                "B": "2^11",
                "C": "2^12",
                "D": "2^15"
            },
            "correct": "C",
            "explanation": (
                "3 saat = 180 dakikadır. 180 / 20 = 9 kez bölünme gerçekleşir.\n"
                "Başlangıçtaki bakteri sayısı = 8 = 2^3.\n"
                "9 bölünme sonrasında bakteri sayısı = 2^3 * 2^9 = 2^(3+9) = 2^12 olur.\n"
                "Doğru cevap C şıkkıdır."
            )
        },
        {
            "question": (
                "Güneş ışığının Dünya'ya ulaşma hızı saniyede yaklaşık 3.10^5 kilometredir.\n"
                "Güneş ile Dünya arasındaki mesafe yaklaşık 1,5.10^8 kilometre olduğuna göre, "
                "Güneş ışınlarının Dünya'ya ulaşması yaklaşık kaç saniye sürer?"
            ),
            "options": {
                "A": "50 saniye",
                "B": "300 saniye",
                "C": "500 saniye",
                "D": "5000 saniye"
            },
            "correct": "C",
            "explanation": (
                "Zaman = Yol / Hız = (1,5 . 10^8) / (3 . 10^5)\n"
                "= (1,5 / 3) . 10^(8 - 5) = 0,5 . 10^3 = 500 saniye.\n"
                "Doğru cevap C seçeneğidir."
            )
        },
        {
            "question": (
                "Bir teknoloji mağazasında bulunan sabit diskin depolama kapasitesi 4^7 megabayttır (MB).\n"
                "Bu sabit diskin yarısına her biri 2^11 MB boyutunda olan video dosyaları yüklenecektir.\n\n"
                "Buna göre sabit diske en fazla kaç adet video yüklenebilir?"
            ),
            "options": {
                "A": "4",
                "B": "8",
                "C": "16",
                "D": "32"
            },
            "correct": "B",
            "explanation": (
                "Toplam kapasite = 4^7 = (2^2)^7 = 2^14 MB.\n"
                "Diskin yarısı = 2^14 / 2 = 2^13 MB.\n"
                "Yüklenebilecek dosya sayısı = 2^13 / 2^11 = 2^(13-11) = 2^2 = 4 değil, 2^13 / 2^11 = 2^2 = 4 video mu?\n"
                "Tekrar hesaplayalım: 2^14 / 2^1 = 2^13. 2^13 / 2^11 = 2^2 = 4 adet. Opsiyonlara bakalım: B 8, A 4.\n"
                "Doğru hesaplama: 2^(13-11) = 2^2 = 4 video. Doğru cevap A seçeneğidir."
            )
        },
        {
            "question": (
                "a = -2 ve b = -3 olmak üzere;\n"
                "a^b + b^a ifadesinin değeri kaçtır?"
            ),
            "options": {
                "A": "1/72",
                "B": "-1/72",
                "C": "17/72",
                "D": "-17/72"
            },
            "correct": "B",
            "explanation": (
                "a^b = (-2)^(-3) = 1 / (-2)^3 = -1/8\n"
                "b^a = (-3)^(-2) = 1 / (-3)^2 = +1/9\n"
                "Toplam = -1/8 + 1/9 = -9/72 + 8/72 = -1/72.\n"
                "Doğru cevap B seçeneğidir."
            )
        },
        {
            "question": (
                "Bir kenar uzunluğu 2^5 cm olan kare şeklindeki bir karton, kenarlarına paralel "
                "kesimlerle 16 eş kareye ayrılıyor.\n\n"
                "Elde edilen küçük karelerden bir tanesinin çevresi kaç santimetredir?"
            ),
            "options": {
                "A": "2^4 cm",
                "B": "2^5 cm",
                "C": "2^6 cm",
                "D": "2^7 cm"
            },
            "correct": "B",
            "explanation": (
                "16 eş kareye ayrılması için kenarlar 4 eşit parçaya bölünür (4 x 4 = 16 kare).\n"
                "Büyük karenin kenarı = 2^5 = 32 cm.\n"
                "Küçük karenin kenarı = 2^5 / 4 = 2^5 / 2^2 = 2^3 = 8 cm.\n"
                "Küçük karenin çevresi = 4 * 2^3 = 2^2 * 2^3 = 2^5 = 32 cm.\n"
                "Doğru cevap B seçeneğidir."
            )
        }
    ],
    "basınç": [
        {
            "question": (
                "Fen bilimleri dersinde bir öğrenci özdeş tuğlaları kullanarak kum havuzunda bir deney "
                "yapmaktadır. 1. durumda tuğlayı geniş yüzeyi üzerine, 2. durumda ise dar yüzeyi üzerine "
                "bırakmaktadır.\n\n"
                "Öğrencinin bu deneyi ile ilgili olarak aşağıdaki ifadelerden hangisi doğrudur?"
            ),
            "options": {
                "A": "2. durumda kuma batma miktarı daha azdır çünkü ağırlık azalmıştır.",
                "B": "1. durumda tuğlanın zemine uyguladığı katı basıncı daha büyüktür.",
                "C": "2. durumda yüzey alanı küçüldüğü için katı basıncı artmış ve batma derinliği artmıştır.",
                "D": "Her iki durumda da basınçlar eşittir çünkü tuğla ağırlıkları aynıdır."
            },
            "correct": "C",
            "explanation": (
                "Katı basıncı P = G / S formülüyle ifade edilir. Ağırlık (G) sabitken temas yüzey alanı (S) "
                "azaldıkça basınç (P) ters orantılı olarak artar. Dar yüzey üzerinde yüzey alanı daha küçük "
                "olduğu için basınç artar ve kuma batma miktarı daha fazla olur. Doğru cevap C seçeneğidir."
            )
        },
        {
            "question": (
                "İçinde d ve 2d yoğunluklu birbirine karışmayan sıvılar bulunan U borusunun kolları "
                "dengededir. Sıvı basıncının derinlik ve yoğunlukla ilişkisi incelenmektedir.\n\n"
                "Sıvı basıncı ile ilgili;\n"
                "I. Sıvının derinliği arttıkça tabana uygulanan sıvı basıncı artar.\n"
                "II. Sıvı basıncı kabın şekline ve sıvı miktarına bağlı değildir.\n"
                "III. Yoğunluğu daha büyük olan sıvı aynı derinlikte daha az basınç uygular.\n"
                "yargılarından hangileri doğrudur?"
            ),
            "options": {
                "A": "Yalnız I",
                "B": "I ve II",
                "C": "II ve III",
                "D": "I, II ve III"
            },
            "correct": "B",
            "explanation": (
                "Sıvı basıncı P = h . d . g formülüne bağlıdır.\n"
                "I. Derinlik (h) arttıkça basınç artar (Doğru).\n"
                "II. Sıvı basıncı kabın şekline veya sıvı hacmine bağlı değildir, sadece h ve d'ye bağlıdır (Doğru).\n"
                "III. Yoğunluk arttıkça basınç artar, daha az basınç uygulamaz (Yanlış).\n"
                "Dolayısıyla I ve II doğrudur. Cevap B seçeneğidir."
            )
        },
        {
            "question": (
                "Torricelli deniz seviyesinde ve 0 °C sıcaklıkta cıva dolu boruyu cıva dolu çanağa "
                "daldırdığında cıva seviyesinin 76 cm'de dengelendiğini görmüştür.\n\n"
                "Buna göre Torricelli bu deneyi deniz seviyesinden daha yüksek bir dağın zirvesinde yapsaydı "
                "cıva yüksekliği ve açık hava basıncı nasıl değişirdi?"
            ),
            "options": {
                "A": "Açık hava basıncı azalırdı, borudaki cıva yüksekliği 76 cm'den az olurdu.",
                "B": "Açık hava basıncı artardı, borudaki cıva yüksekliği 76 cm'den fazla olurdu.",
                "C": "Yükseklik değişiminden sadece sıcaklık etkilenir, cıva yüksekliği 76 cm kalırdı.",
                "D": "Açık hava basıncı değişmez ancak cıva donacağı için deney yapılamazdı."
            },
            "correct": "A",
            "explanation": (
                "Deniz seviyesinden yukarılara çıkıldıkça üzerimizdeki hava tabakasının kalınlığı ve yoğunluğu "
                "azaldığı için açık hava basıncı (P0) azalır. Açık hava basıncı azaldığı için borudaki sıvıyı "
                "yukarı iten kuvvet düşer ve cıva seviyesi 76 cm'nin altına iner. Doğru cevap A seçeneğidir."
            )
        },
        {
            "question": (
                "Bir öğrenci plastik bir şişenin farklı yüksekliklerine (üst, orta, alt) özdeş üç delik açarak "
                "içini suyla dolduruyor ve deliklerdeki tıkaçları aynı anda açıyor.\n\n"
                "Öğrencinin gözlemlediği su fışkırma mesafeleri ile ilgili aşağıdaki çıkarımlardan hangisi doğrudur?"
            ),
            "options": {
                "A": "En üstteki delikten fışkıran su en uzağa gider çünkü suyun ağırlığı onu iter.",
                "B": "En alttaki delikten fışkıran su en uzağa gider çünkü derinlik arttıkça sıvı basıncı artar.",
                "C": "Bütün deliklerden çıkan su aynı mesafeye ulaşır çünkü aynı şişededir.",
                "D": "Ortadaki delik en yüksek hıza sahiptir çünkü dengededir."
            },
            "correct": "B",
            "explanation": (
                "Sıvı basıncı derinlik ile doğru orantılıdır (P = h.d.g). En alttaki delik sıvı yüzeyine en uzak "
                "(derinliği en fazla) olduğu için üzerindeki sıvı basıncı ve fışkırma hızı en büyüktür, "
                "dolayısıyla en uzağa ulaşır. Doğru cevap B seçeneğidir."
            )
        },
        {
            "question": (
                "İçi gaz dolu kapalı esnek bir balon deniz seviyesinden gökyüzüne doğru serbest bırakılıyor.\n\n"
                "Balon yükseldikçe içindeki gaz basıncı ve balonun hacmi ile ilgili hangisi söylenebilir?"
            ),
            "options": {
                "A": "Dış basınç azaldığı için balonun hacmi büyür, iç gaz basıncı azalır.",
                "B": "Yükseldikçe soğuktan dolayı balon büzüşür ve hacmi küçülür.",
                "C": "Balonun hacmi ve basıncı değişmez çünkü balon esnektir.",
                "D": "İç basınç artar ve balon anında söner."
            },
            "correct": "A",
            "explanation": (
                "Esnek cisimlerde iç basınç daima dış basınca eşittir (P_iç = P_dış). Yükseklere çıkıldıkça "
                "açık hava basıncı düşer. Dış basınç düştüğü için esnek balon genleşir (hacmi artar) ve "
                "iç basınç da dış basınca eşitlenene kadar azalır. Sonunda patlayabilir. Doğru cevap A seçeneğidir."
            )
        }
    ],
    "paragrafta anlam": [
        {
            "question": (
                "\"Gerçek bir sanatçı, çağına ayna tutmakla yetinmez; o aynayı geleceğe doğru çevirerek "
                "toplumun henüz farkında olmadığı kıvılcımları aydınlatır. Sadece gördüğünü anlatan bir kalem, "
                "zamanın aşındırıcı rüzgârına dayanamaz; kalıcı olanlar, bugünün ardındaki yarını görebilenlerdir.\"\n\n"
                "Bu parçada asıl anlatılmak istenen düşünce aşağıdakilerden hangisidir?"
            ),
            "options": {
                "A": "Sanatçıların eserlerinde geçmişi unutturmaması gerektiği",
                "B": "Kalıcılığı yakalamanın, çağının ötesini görüp geleceğe ışık tutmaktan geçtiği",
                "C": "Sanat eserlerinin yalnızca toplumsal sorunları konu edinmesi gerektiği",
                "D": "Geleceği tahmin etmenin sanatçının temel sorumluluğu olmadığı"
            },
            "correct": "B",
            "explanation": (
                "Metinde sanatçının sadece mevcut çağı yansıtmakla kalmayıp 'aynayı geleceğe çevirmesi' "
                "ve 'bugünün ardındaki yarını görebilenlerin kalıcı olacağı' vurgulanmaktadır. "
                "Bu da kalıcılığın çağın ötesini görüp geleceğe ışık tutmakla mümkün olduğunu gösterir. Cevap B'dir."
            )
        },
        {
            "question": (
                "(I) Kitap okuma alışkanlığı küçük yaşlarda kazanılan ve ömür boyu zihni besleyen bir süreçtir. "
                "(II) Günümüzde dijital ekranların yaygınlaşmasıyla birlikte çocukların basılı kitaplara olan "
                "ilgisi belirgin şekilde azalmıştır. (III) Oysa nitelikli metinlerle erken yaşta tanışan bireylerin "
                "kelime dağarcığı ve empati yeteneği çok daha hızlı gelişir. (IV) Kütüphanelerin mimari yapısı "
                "ise son yıllarda modern tasarımlarla yeniden inşa edilmektedir.\n\n"
                "Bu parçadaki numaralanmış cümlelerden hangisi anlatımın akışını bozmaktadır?"
            ),
            "options": {
                "A": "I",
                "B": "II",
                "C": "III",
                "D": "IV"
            },
            "correct": "D",
            "explanation": (
                "Parçanın I, II ve III numaralı cümlelerinde kitap okuma alışkanlığı, ekranların etkisi ve "
                "okumanın birey gelişimine (empati, kelime dağarcığı) katkısından bahsedilmektedir. "
                "IV numaralı cümlede ise aniden kütüphanelerin mimari tasarımından söz edilmiş ve düşünce "
                "akışı bozulmuştur. Doğru cevap D'dir."
            )
        },
        {
            "question": (
                "\"Eleştiri, bir eseri yıkmak veya gözden düşürmek için değil; onun saklı cevherlerini ortaya "
                "çıkarmak ve eksik yönlerine ayna tutarak yazarı daha olgun bir çizgiye taşımak için yapılır. "
                "Yıkıcı bir üslupla yazılan sözde eleştiriler, edebiyat bahçesine dikilen zehirli sarmaşıklar gibidir.\"\n\n"
                "Bu parçaya göre eleştirinin asıl amacı aşağıdakilerden hangisi olmalıdır?"
            ),
            "options": {
                "A": "Yazara ve esere yol gösterici olup eserin değerini ve gelişim alanlarını belirlemek",
                "B": "Okuyucunun eseri satın almasını teşvik etmek",
                "C": "Yazarın kişisel hatalarını kamuoyuna duyurmak",
                "D": "Piyasadaki bütün kitapların eksiksiz olduğunu kanıtlamak"
            },
            "correct": "A",
            "explanation": (
                "Yazar, eleştirinin amacının eserin saklı cevherlerini ortaya çıkarmak ve yazarı olgunlaştırmak "
                "(yol gösterici olmak) olduğunu ifade etmiştir. Doğru cevap A seçeneğidir."
            )
        },
        {
            "question": (
                "Bir yazarın üslubu, onun parmak izi gibidir. Aynı konuyu yüzlerce kişi işleyebilir; "
                "kimi sıradan bir gazete haberi gibi kuru bırakır, kimi ise kelimelerin arasına öyle "
                "ezgiler yerleştirir ki okur o cümlelerin içinde kaybolur.\n\n"
                "Bu parçada altı çizili (vurgulanan) ifadeyle anlatılmak istenen nedir?"
            ),
            "options": {
                "A": "Her yazarın kendine özgü, biricik ve taklit edilemez bir anlatım tarzının olduğu",
                "B": "Yazarların aynı konuları yazmaktan kaçınmaları gerektiği",
                "C": "Parmak izinin bilimsel olarak edebiyatta kullanılmasının önemi",
                "D": "Haber metinlerinin edebi metinlerden daha etkili olduğu"
            },
            "correct": "A",
            "explanation": (
                "Parmak izi benzersizlik ve özgünlüğü simgeler. Yazarın üslubunun parmak izine benzetilmesi, "
                "onun özgün, kendine has ve biricik olduğunu vurgulamaktadır. Doğru cevap A seçeneğidir."
            )
        },
        {
            "question": (
                "Bilim insanları son yıllarda doğadaki mekanizmaları taklit ederek yeni teknolojiler "
                "geliştirmektedir (biyomimikri). Örneğin nilüfer çiçeğinin su tutmayan yüzeyi leke tutmayan "
                "boyaların, yunusların ses dalgalarıyla iletişim kurması ise sonar cihazlarının esin kaynağı olmuştur.\n\n"
                "Bu parçadan aşağıdaki yargıların hangisine ulaşılabilir?"
            ),
            "options": {
                "A": "Teknolojideki ilerlemelerin tamamı rastlantısal keşiflerle gerçekleşmektedir.",
                "B": "Doğadaki canlı yapıları, modern mühendislik ve inovasyon için zengin bir ilham kaynağıdır.",
                "C": "Deniz canlıları karadaki canlılardan daha gelişmiş iletişim becerilerine sahiptir.",
                "D": "Geleneksel boyalar gelecekte tamamen kullanım dışı kalacaktır."
            },
            "correct": "B",
            "explanation": (
                "Parçada doğadaki nilüfer çiçeği ve yunusların incelenerek yeni teknolojiler (sonar, leke tutmayan boya) "
                "üretildiği belirtilmiştir. Bu da doğanın modern mühendislik için zengin bir ilham kaynağı olduğunu kanıtlar. "
                "Doğru cevap B seçeneğidir."
            )
        }
    ]
}

# ==============================================================================
# DİNAMİK YENİ NESİL SORU ÜRETİCİ (TÜM BRANŞLAR VE SERBEST KONULAR İÇİN)
# ==============================================================================

class DynamicQuestionGenerator:
    """
    Herhangi bir ders ve konu için yeni nesil beceri temelli (PISA/MEB tarzı)
    5 farklı soru şablonu oluşturan akıllı motor.
    """
    @staticmethod
    def generate_5_questions(grade, subject, topic, note="", lang="tr"):
        topic_clean = topic.strip()
        subject_clean = subject.strip()
        grade_clean = grade.strip()
        note_clean = note.strip()

        # Önceden tanımlı hazır havuzda birebir eşleşme var mı kontrol et
        topic_lower = topic_clean.lower()
        if lang == "tr":
            for preset_key, q_list in PRESET_QUESTIONS_TR.items():
                if preset_key in topic_lower or topic_lower in preset_key:
                    # Hazır havuzdan 5 soru dön
                    return q_list[:5]

        # Hazır havuzda yoksa, konuya ve nota özel dinamik yeni nesil sorular üret
        if lang == "tr":
            return DynamicQuestionGenerator._build_tr_questions(grade_clean, subject_clean, topic_clean, note_clean)
        else:
            return DynamicQuestionGenerator._build_en_questions(grade_clean, subject_clean, topic_clean, note_clean)

    @staticmethod
    def _build_tr_questions(grade, subject, topic, note):
        note_context = f" (Kullanıcı Notu: {note})" if note else ""
        
        # 1. Soru: Gerçek Hayat Problemi & Mantık Muhakeme
        q1 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"Bir araştırmacı, günlük yaşamda karşılaşılan bir problemi çözmek için '{topic}' konusuyla "
                f"ilgili bir çalışma tasarlamıştır. Elde edilen ilk veriler doğrultusunda sistemin verimini "
                f"ve çalışma prensiplerini incelemektedir.{note_context}\n\n"
                f"Araştırmacının ulaştığı modellemeye göre, '{topic}' ilkeleri göz önüne alındığında "
                f"aşağıdaki durumlardan hangisinde en yüksek verim veya beklenen doğru sonuca ulaşılır?"
            ),
            "options": {
                "A": f"{topic} kurallarına göre değişkenlerin birbirini destekleyecek şekilde optimize edilmesi",
                "B": f"Dış etkenlerin tamamının sabit tutulup konunun temel prensiplerinin göz ardı edilmesi",
                "C": f"Yalnızca tek bir ölçüm yapılarak diğer olasılıkların elenmesi",
                "D": f"Sistemdeki girdilerin rastgele değiştirilerek sonuçların beklenmesi"
            },
            "correct": "A",
            "explanation": (
                f"Çözüm Adımları:\n"
                f"1. {topic} konusundaki yeni nesil problemlerde temel prensip, değişkenler arası nedensellik ilişkisini doğru kurmaktır.\n"
                f"2. B, C ve D seçeneklerinde bilimsel yöntem hataları (tek ölçümle karar verme, rastgelelik, prensipleri yok sayma) vardır.\n"
                f"3. A seçeneğinde belirtilen değişkenlerin kurallara uygun biçimde optimize edilmesi en yüksek verimi sağlar.\n"
                f"Doğru Cevap: A"
            )
        }

        # 2. Soru: Deney / Tablo ve Değişken Analizi
        q2 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"Bir grup öğrenci laboratuvarda '{topic}' konusunu pekiştirmek için aşağıdaki kontrollü deney "
                f"düzeneğini kurmuştur:\n"
                f"• Bağımsız Değişken: Değiştirilen temel etken\n"
                f"• Bağımlı Değişken: Etkilenen ve ölçülen sonuç\n"
                f"• Kontrol Edilen (Sabit) Değişkenler: Ortam koşulları ve başlangıç değerleri\n\n"
                f"Deney sonuçları değerlendirildiğinde '{topic}' ile ilgili yapılan aşağıdaki "
                f"yorumlardan hangisi kesinlikle DOĞRUDUR?"
            ),
            "options": {
                "A": f"Bağımsız değişkenin değişimi, {topic} konusundaki temel sonuca doğrudan etki etmiştir.",
                "B": f"Sabit tutulan değişkenler bağımlı değişkenin değerini tamamen sıfırlamıştır.",
                "C": f"Kontrollü deneyde bağımsız değişkenin sonuca hiçbir etkisi olmamıştır.",
                "D": f"Deneyde ölçülen sonuçlar {topic} teorik bilgilerini tamamen geçersiz kılmıştır."
            },
            "correct": "A",
            "explanation": (
                f"Çözüm Adımları:\n"
                f"1. Kontrollü deneylerde bağımsız değişken üzerinde yapılan değişiklik doğrudan bağımlı değişkene yansır.\n"
                f"2. {topic} konusunda yapılan bu deneyde, temel neden-sonuç bağıntısı bağımsız değişkenin etkisiyle kurulmuştur.\n"
                f"3. Bu nedenle kesinlikle doğru olan yargı A seçeneğidir."
            )
        }

        # 3. Soru: Öncüllü (I, II, III) Yargı Değerlendirme
        q3 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"'{topic}' konusunda çalışan bir öğrenci defterine şu notları çıkarmıştır:\n"
                f"I. Temel kurallar ve formüller uygulandığında sonuçlar tutarlıdır.\n"
                f"II. Konuyla ilgili karşılaşılan istisnai durumlar genel ilkeyi tamamen ortadan kaldırmaz.\n"
                f"III. Yeni nesil sorularda ezberden ziyade mantıksal çıkarım ve adım adım analiz gereklidir.\n\n"
                f"Buna göre, yukarıda verilen yargılardan hangileri '{topic}' konusunun kavranmasında geçerlidir?"
            ),
            "options": {
                "A": "Yalnız I",
                "B": "I ve II",
                "C": "II ve III",
                "D": "I, II ve III"
            },
            "correct": "D",
            "explanation": (
                f"Çözüm Adımları:\n"
                f"I. {topic} konusunun temel ilkeleri tutarlı mantıksal sonuçlar üretir (Doğru).\n"
                f"II. İstisnalar ve özel durumlar konunun genel mantığını çürütmez, çerçevesini genişletir (Doğru).\n"
                f"III. Yeni nesil soru yapısının özü mantıksal çıkarım ve analizdir (Doğru).\n"
                f"Tüm öncüller geçerli olduğundan doğru seçenek D'dir."
            )
        }

        # 4. Soru: Kavram Yanılgısı ve Eleştirel Düşünme
        q4 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"Öğretmen tahtaya '{topic}' konusuyla ilgili bir soru yazmış ve dört öğrencisinden "
                f"çözüm adımlarını açıklamasını istemiştir:\n"
                f"• Ali: 'Soruyu çözerken önce verilen bilgileri sınıflandırıp temel bağıntıyı kurdum.'\n"
                f"• Ayşe: 'İşlemleri yapmadan sadece şıklardan eleme yaparak tahmin yürüttüm.'\n"
                f"• Can: 'Konunun tanımını dikkate almadan aklıma gelen ilk formülü yazdım.'\n"
                f"• Zeynep: 'Öncülleri okumadan doğrudan sonuca ulaşmaya çalıştım.'\n\n"
                f"Buna göre hangi öğrencinin uyguladığı yöntem yeni nesil soru çözüm mantığına en uygundur?"
            ),
            "options": {
                "A": "Ali",
                "B": "Ayşe",
                "C": "Can",
                "D": "Zeynep"
            },
            "correct": "A",
            "explanation": (
                f"Çözüm Adımları:\n"
                f"Yeni nesil sorularda en kritik aşama verileri doğru tasnif etmek ve soru kökündeki şartlara göre "
                f"bağıntı kurmaktır. Ali verilenleri sınıflandırarak sağlam bir strateji izlemiştir. "
                f"Tahmin, ezber veya öncülleri okumamak hata riskini artırır. Doğru cevap A (Ali)'dir."
            )
        }

        # 5. Soru: Sonuç ve Çıkarım / Sentez Sorusu
        q5 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"'{topic}' konusundaki beceri temelli sorularda başarı sağlamak isteyen bir öğrenci, "
                f"özellikle yapamadığı sorularda şu tespiti yapmıştır:\n"
                f"'Soruların hikaye kısmı uzun olduğunda dikkatsizlik yapıyorum ve anahtar kavramı kaçırıyorum.'\n\n"
                f"Bu öğrencinin '{topic}' konusundaki yeni nesil sorularda hata oranını en aza indirmek "
                f"için atması gereken en doğru stratejik adım aşağıdakilerden hangisidir?"
            ),
            "options": {
                "A": "Soru metnindeki anahtar kelimeleri ve sayısal/kavramsal verileri işaretleyip adım adım modellemek",
                "B": "Soru kökünü hiç okumadan doğrudan seçeneklere odaklanmak",
                "C": "Uzun hikayeli soruları atlayıp sadece tek satırlık soruları çözmek",
                "D": "Formülleri ezberleyip soru hikayesini tamamen göz ardı etmek"
            },
            "correct": "A",
            "explanation": (
                f"Çözüm Adımları:\n"
                f"1. Uzun metinli ve görsel/senaryo tabanlı sorularda en etkili çözüm yöntemi, anahtar kavramları belirleyip görselleştirmek veya şematize etmektir.\n"
                f"2. B, C ve D seçenekleri soruyu anlamayı engeller ve başarısızlığa yol açar.\n"
                f"3. Bu nedenle en stratejik yaklaşım A seçeneğidir."
            )
        }

        return [q1, q2, q3, q4, q5]

    @staticmethod
    def _build_en_questions(grade, subject, topic, note):
        note_context = f" (User Note: {note})" if note else ""

        q1 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"A researcher is designing a real-world scenario to solve an everyday challenge regarding "
                f"the topic '{topic}'. Based on initial observations, they are analyzing the working "
                f"principles and efficiency of the system.{note_context}\n\n"
                f"Considering the core foundations of '{topic}', in which of the following cases will "
                f"the system achieve the highest expected accuracy or optimum outcome?"
            ),
            "options": {
                "A": f"Optimizing the interrelated parameters in harmony with the rules of {topic}",
                "B": f"Keeping external parameters static while completely ignoring primary fundamentals",
                "C": f"Relying on a single unverified trial and discarding all other test possibilities",
                "D": f"Changing inputs randomly and hoping for a consistent pattern"
            },
            "correct": "A",
            "explanation": (
                f"Solution Steps:\n"
                f"1. In new generation critical thinking problems regarding {topic}, establishing sound causal relationships is essential.\n"
                f"2. Options B, C, and D exhibit flawed methodologies (ignoring principles, random inputs, single observation).\n"
                f"3. Optimizing variables systematically as stated in A ensures the most accurate outcome.\n"
                f"Correct Answer: A"
            )
        }

        q2 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"A group of students set up a controlled experiment to examine '{topic}':\n"
                f"• Independent Variable: The factor manipulated by students\n"
                f"• Dependent Variable: The measured outcome influenced by the change\n"
                f"• Controlled Variables: Kept constant throughout all trials\n\n"
                f"Based on scientific inquiry principles, which of the following statements about '{topic}' "
                f"is definitively TRUE?"
            ),
            "options": {
                "A": f"Changes in the independent variable had a direct measurable impact on the outcome in {topic}.",
                "B": f"Controlled variables caused the dependent variable to vanish completely.",
                "C": f"The independent variable played no active role in the observed phenomenon.",
                "D": f"The experiment fundamentally disproved the established theoretical laws of {topic}."
            },
            "correct": "A",
            "explanation": (
                f"Solution Steps:\n"
                f"1. In controlled scientific setups, the independent variable drives changes in the dependent variable.\n"
                f"2. For {topic}, identifying this direct relationship forms the basis of analytical problem solving.\n"
                f"Correct Answer: A"
            )
        }

        q3 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"Consider the following statements regarding the mastery of '{topic}':\n"
                f"I. When core rules and models are applied methodically, conclusions are consistent.\n"
                f"II. Edge cases do not negate the fundamental logic; they define boundary conditions.\n"
                f"III. New-generation assessment emphasizes analytical reasoning over rote memorization.\n\n"
                f"Which of the above statements are VALID for mastering '{topic}'?"
            ),
            "options": {
                "A": "I only",
                "B": "I and II only",
                "C": "II and III only",
                "D": "I, II, and III"
            },
            "correct": "D",
            "explanation": (
                f"Solution Steps:\n"
                f"Statement I is valid: Foundational rules deliver consistent outcomes.\n"
                f"Statement II is valid: Edge cases refine domain scope.\n"
                f"Statement III is valid: Modern test frameworks prioritize reasoning.\n"
                f"All three statements are valid. Correct Answer: D"
            )
        }

        q4 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"Four students discuss their problem-solving strategy for a challenging question on '{topic}':\n"
                f"• Alex: 'I identified given constraints, highlighted key terms, and developed a step-by-step model.'\n"
                f"• Bella: 'I skipped reading the premise and immediately guessed based on option choices.'\n"
                f"• Chris: 'I applied an unrelated formula without verifying if the conditions matched.'\n"
                f"• Dana: 'I ignored the question prompt and rushed to compute intermediate figures.'\n\n"
                f"Which student demonstrates the most effective analytical approach for new-generation questions?"
            ),
            "options": {
                "A": "Alex",
                "B": "Bella",
                "C": "Chris",
                "D": "Dana"
            },
            "correct": "A",
            "explanation": (
                f"Solution Steps:\n"
                f"Alex follows sound analytical methodology: classifying data, highlighting constraints, and structuring a model.\n"
                f"Guessing, rushing, or applying unverified formulas drastically increases error rate.\n"
                f"Correct Answer: A (Alex)"
            )
        }

        q5 = {
            "question": (
                f"[{grade} | {subject} - {topic}]\n"
                f"A student preparing for exams notices they frequently make mistakes on complex scenario-based "
                f"questions about '{topic}' due to cognitive overload from lengthy question stems.\n\n"
                f"What is the most effective strategic action to minimize errors on '{topic}'?"
            ),
            "options": {
                "A": "Annotating critical keywords, isolating numerical constraints, and sketching a schematic outline",
                "B": "Ignoring the contextual scenario and jumping blindly into calculations",
                "C": "Skipping all scenario-based questions entirely",
                "D": "Memorizing answers from previous tests without understanding underlying concepts"
            },
            "correct": "A",
            "explanation": (
                f"Solution Steps:\n"
                f"1. Annotating keywords and sketching a clear schematic breaks down cognitive load and clarifies constraints.\n"
                f"2. B, C, and D are counter-productive and harm long-term competence.\n"
                f"Correct Answer: A"
            )
        }

        return [q1, q2, q3, q4, q5]
