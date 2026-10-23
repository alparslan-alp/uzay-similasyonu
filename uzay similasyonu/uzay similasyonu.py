from ursina import *
import math
import os
import json
from datetime import datetime, timedelta
import random

app = Ursina()

window.title = '3D Profesyonel Simülasyon - Dinamik Samanyolu Gökyüzü'
window.borderless = False
window.fullscreen = False

# Simülasyon Durdurma ve Zaman Durumu
simulasyon_durdu = False
hiz_carpani = 100.0
simulasyon_saniyesi = 0.0
baslangic_tarihi = datetime(2026, 1, 1)

son_guncellenen_gun = -1

# --- JSON HAFIZA YÖNETİMİ ---
DOSYA_ADI = "haber_hafizasi.json"


def hafizayi_yukle():
    if os.path.exists(DOSYA_ADI):
        try:
            with open(DOSYA_ADI, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "sehirler": [],
        "kayiplar": [],
        "hirsizlar": [],
        "kazazedeler": []
    }


def hafizayi_kaydet(veri):
    try:
        with open(DOSYA_ADI, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
    except:
        pass


# --- AKILLI VE DOĞAL TÜRKÇE İSİM ÜRETİCİSİ ---
ISIM_KOKLERI_1 = [
    "Alp", "Berk", "Can", "Demir", "Eren", "Gök", "Kaan", "Mert", "Ege",
    "Umut", "Toprak", "Deniz", "Cem", "Kor", "Bora", "Doruk", "Kerem",
    "Yusuf", "Ahmet", "Mehmet", "Emre", "Burak", "Arda", "Zeynep", "Elif",
    "Ayşe", "Merve", "Selin", "Büşra", "Cemre", "İrem", "Ece", "Defne",
    "Yağmur", "Melis", "Aybüke", "Göktuğ", "Alperen", "Tolgahan", "Batuhan"
]

ISIM_KOKLERI_2 = [
    "er", "tan", "han", "kan", "mert", "can", "ay", "alp", "nur", "su",
    "ç", "bey", "gül", "deniz", "şah", "barış", "ulaş", "efe", "kaan"
]

SOYAD_KOKLERI = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım",
    "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan",
    "Çetin", "Koç", "Kurt", "Özkan", "Şimşek", "Polat", "Özcan", "Korkmaz",
    "Demiroğlu", "Aksu", "Yurdakul", "Koçyiğit", "Soylu", "Aksoy", "Erdem"
]

SEHIR_KOKLERI = [
    "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Trabzon",
    "Samsun", "Kayseri", "Eskişehir", "Gaziantep", "Mersin", "Denizli"
]

SEHIR_EKLERI = ["kent", "şehir", "ova", "hisar", "liman", "merkez", "eli", "başı"]

SIKET_SEKTORLERI = ["Holding", "Enerji", "Teknoloji", "Lojistik", "Finans", "Otomotiv", "Madencilik", "Yazılım",
                    "Havacılık"]


def rastgele_isim_uret():
    if random.random() < 0.5:
        isim = random.choice(ISIM_KOKLERI_1)
    else:
        isim = random.choice(ISIM_KOKLERI_1) + random.choice(ISIM_KOKLERI_2)
    soyad = random.choice(SOYAD_KOKLERI)
    return f"{isim} {soyad}"


def rastgele_sehir_uret():
    if random.random() < 0.6:
        return random.choice(SEHIR_KOKLERI)
    else:
        baslangic = random.choice(["Kara", "Ak", "Altın", "Yurt", "Demir", "Kuzey", "Güneş"])
        ek = random.choice(SEHIR_EKLERI)
        return baslangic + ek.capitalize()


def rastgele_sirket_uret():
    bas = random.choice(["Global", "Anadolu", "Alfa", "Mega", "Delta", "Nova", "Prime", "Vertex"])
    sektor = random.choice(SIKET_SEKTORLERI)
    return f"{bas} {sektor}"


# --- PROFESYONEL VE GERÇEKÇİ HABER MOTORU ---
def rastgele_haber_uret():
    hafiza = hafizayi_yukle()
    devam_ihtimali = random.random()

    if devam_ihtimali < 0.45 and (
            hafiza["kayiplar"] or hafiza["hirsizlar"] or hafiza["kazazedeler"] or hafiza["sehirler"]):
        senaryo = random.randint(1, 4)

        if senaryo == 1 and hafiza["kayiplar"] and hafiza["sehirler"]:
            kayip = random.choice(hafiza["kayiplar"])
            yeni_sehir = random.choice(hafiza["sehirler"])
            hafiza["kayiplar"].remove(kayip)
            hafizayi_kaydet(hafiza)

            eski_s = kayip.get('eski_sehir', kayip.get('sehir', 'Bilinmeyen Şehir'))
            baslik = f"GÜZEL HABER: Günlerdir Aranan {kayip['isim']} {yeni_sehir}'de Bulundu"
            detay = f"[{yeni_sehir} Emniyet Müdürlüğü - Basın Bülteni]\n{eski_s}'de kayıp olarak aranmakta olan {kayip['isim']}, {yeni_sehir} il emniyet müdürlüğünün itinalı çalışmaları sonucu sağ olarak tespit edildi. Sağlık durumunun iyi olduğu ve ailesiyle irtibat kurulduğu bildirildi."
            return {"baslik": baslik, "detay": detay}

        elif senaryo == 2 and hafiza["hirsizlar"] and hafiza["sehirler"]:
            hirsiz = random.choice(hafiza["hirsizlar"])
            yeni_sehir = random.choice(hafiza["sehirler"])
            hafiza["hirsizlar"].remove(hirsiz)
            hafizayi_kaydet(hafiza)

            eski_s = hirsiz.get('eski_sehir', hirsiz.get('sehir', 'Bilinmeyen Şehir'))
            kod = hirsiz.get('kod_adi', 'Şüpheli')
            baslik = f"ŞAFAK OPERASYONU: Aranan Soyguncu {yeni_sehir}'de Ele Geçirildi"
            detay = f"[{yeni_sehir} Asayiş Şube Başsavcılığı]\n{eski_s}'deki büyük vurgunun ardından kırmızı bültenle aranan '{kod}' lakaplı {hirsiz['isim']}, {yeni_sehir} merkezli düzenlenen eş zamanlı operasyonla saklandığı adreste yakalanarak tutuklandı."
            return {"baslik": baslik, "detay": detay}

        elif senaryo == 3 and hafiza["kazazedeler"]:
            kazazede = random.choice(hafiza["kazazedeler"])
            hafiza["kazazedeler"].remove(kazazede)
            hafizayi_kaydet(hafiza)

            kazazede_sehir = kazazede.get('sehir', 'Merkez')
            sonuc = random.choice(["kurtuldu", "vefat"])
            if sonuc == "kurtuldu":
                baslik = f"MUCİZE KURTULUŞ: Yoğun Bakımdan Sevindiren Haber"
                detay = f"[{kazazede_sehir} Şehir Hastanesi Başhekimliği]\nGeçtiğimiz günlerde {kazazede_sehir} otoyolunda yaşanan zincirleme kazada ağır yaralanan {kazazede['isim']}, 14 günlük yaşam mücadelesini kazanarak normal odaya alındı."
            else:
                baslik = f"ACI KAYIP: Hastaneden Acı Haber Geldi"
                detay = f"[{kazazede_sehir} Araştırma Hastanesi]\n{kazazede_sehir}'deki kazada ağır yaralı olarak tedavi altına alınan {kazazede['isim']}, yapılan tüm müdahalelere rağmen kurtarılamayarak hayatını kaybetti. Başsağlığı dileriz."
            return {"baslik": baslik, "detay": detay}

        elif senaryo == 4 and hafiza["sehirler"]:
            sehir = random.choice(hafiza["sehirler"])
            sirket = rastgele_sirket_uret()
            oran = random.randint(5, 40)

            baslik = f"EKONOMİ GÜNDEMİ: {sehir}'de {sirket} Dev Yatırıma Başlıyor"
            detay = f"[{sehir} Ticaret ve Sanayi Odası]\nDaha önce çeşitli olaylarla gündeme gelen {sehir} bölgesinde ekonomik hareketlilik sürerken, {sirket} öncülüğünde %{oran} büyüklüğünde yeni bir sanayi entegrasyon projesi imzalandı."
            return {"baslik": baslik, "detay": detay}

    kategori = random.randint(1, 8)
    sehir = rastgele_sehir_uret()
    isim = rastgele_isim_uret()
    sirket = rastgele_sirket_uret()
    arac_sayisi = random.randint(3, 18)
    yarali_sayisi = random.randint(1, 14)
    para_milyon = random.randint(15, 450)
    yuzde = random.randint(2, 65)

    if sehir not in hafiza["sehirler"]:
        hafiza["sehirler"].append(sehir)

    if kategori == 1:
        hafiza["kazazedeler"].append({"isim": isim, "sehir": sehir})
        baslik = f"SON DAKİKA TRAFİK: {sehir} Otoyolunda Zincirleme Kaza"
        detay = f"[{sehir} Karayolları Genel Müdürlüğü]\n{sehir} kuzey çevre yolunda sis ve buzlanma nedeniyle {arac_sayisi} aracın karıştığı zincirleme trafik kazası meydana geldi. Olay yerine sevk edilen sağlık ekipleri, aralarında {isim} adlı vatandaşın da bulunduğu {yarali_sayisi} yaralıyı çevredeki hastanelere kaldırdı. Yol ulaşıma geçici olarak kapandı."
    elif kategori == 2:
        baslik = f"BİLİM DÜNYASI BU KEŞFİ KONUŞUYOR: {sehir} Arkeolojik Kazıları"
        detay = f"[{sirket} Araştırma Enstitüsü]\n{sehir} kırsalında yürütülen jeolojik ve tarihi kazı çalışmalarında, döneme ait olduğu düşünülen ve bölge ekonomisine %{yuzde} oranında turizm katkısı sunması beklenen devasa kalıntılara ulaşıldı. Kültür bakanlığı bölgeyi koruma altına aldı."
    elif kategori == 3:
        kod_adi = f"Operasyon-{random.randint(1000, 9999)}"
        hafiza["hirsizlar"].append({"isim": isim, "kod_adi": kod_adi, "eski_sehir": sehir})
        baslik = f"BÜYÜK VURGUN: {sehir}'de {para_milyon} Milyonluk Soygun Alarmi"
        detay = f"[{sehir} İl Emniyet Müdürlüğü Asayiş Şube]\n{sehir} merkezindeki kıymetli maden kasasına gece saatlerinde düzenlenen profesyonel soygunla ilgili {para_milyon} milyonluk soygun tespit edildi. Güvenlik kameralarını devre dışı bırakan şüphelinin {isim} olduğu ve '{kod_adi}' adıyla arandığı açıklandı."
    elif kategori == 4:
        baslik = f"METEOROLOJİden KRİTİK UYARI: {sehir}'de Şiddetli Fırtına"
        detay = f"[{sehir} Valiliği Kriz Masası]\n{sehir} genelinde aniden bastıran saatteki hızı 95 kilometreyi bulan fırtına ve şiddetli yağışlar nedeniyle çatı uçmaları ve su baskınları yaşandı. Belediye ekipleri {random.randint(5, 25)} mahallede aralıksız mesai yürütüyor."
    elif kategori == 5:
        hafiza["kayiplar"].append({"isim": isim, "eski_sehir": sehir})
        baslik = f"KAYIP İHBARI: Günlerdir Haber Alınamayan {isim} Aranıyor"
        detay = f"[{sehir} Cumhuriyet Başsavcılığı]\n{sehir}'de ikamet eden {isim}, dün sabahtan bu yana evine dönmedi. Ailesinin kayıp başvurusu üzerine emniyet birimleri geniş çaplı arama ve köprü/kamera incelemesi başlattı. Görenlerin polise haber vermesi istendi."
    elif kategori == 6:
        baslik = f"PİYASALARDA HAREKETLİLİK: {sirket} Hisselerinde Rekor Artış"
        detay = f"[Borsa Finans Analiz Servisi]\n{sehir} borsasında işlem gören {sirket}, açıklanan son çeyrek bilançosu ve yeni küresel ortaklık anlaşması sonrasında hisselerinde %{yuzde} değer kazandı. Uzmanlar yatırımcıları temkinli olmaları yönünde uyarıyor."
    elif kategori == 7:
        baslik = f"BÜYÜK İKRAMİYE SAHİBİNİ BULDU: {sehir} Şubesinde Tarihi An"
        detay = f"[Milli Piyango İdaresi Genel Müdürlüğü]\n{sehir} şubesinden yatırılan şans oyunu kuponuna {para_milyon} milyon TL'lik dev ikramiye isabet etti. Kuponun yatırıldığı bayii akına uğrarken, talihlinin kimliği henüz gizli tutuluyor."
    else:
        baslik = f"STRATEJİK ZİRVE: {sehir}'de Ortak Kalkınma Kararı Alındı"
        detay = f"[{sehir} Kongre ve Kültür Merkezi]\n{sirket} üst düzey yöneticileri ve {sehir} yerel idarecilerinin katıldığı olağanüstü zirvede, bölgenin altyapı sorunlarını çözecek yeni bir ortaklık protokolü resmen imzalandı."

    hafizayi_kaydet(hafiza)
    return {"baslik": baslik, "detay": detay}


# --- UZAY VE DİNAMİK GÖKYÜZÜ KAPLAMALARI ---
def resim_bul(isimler):
    if isinstance(isimler, str):
        isimler = [isimler]
    proje_klasoru = application.asset_folder
    for dosya in os.listdir(proje_klasoru):
        dosya_alt = dosya.lower()
        if dosya_alt.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            for aranan in isimler:
                if aranan.lower() in dosya_alt:
                    return dosya
    return None


# Doku arama isimleri
uzay_resim = resim_bul(['uzay', 'space', 'sky'])
samanyolu_resim = resim_bul(['samanyolu', 'milkyway', 'milky_way', 'galaxy', 'galaksi'])

# Gökyüzü nesnesini oluşturma
sky_entity = Sky(texture=uzay_resim if uzay_resim else None,
                 color=color.white if uzay_resim else color.rgb(5 / 255, 5 / 255, 10 / 255))
mevcut_sky_durumu = "uzay"  # Mevcut aktif arka plan durumunu tutar

for _ in range(350):
    Entity(
        model='sphere',
        color=color.rgb(random.randint(200, 255) / 255, random.randint(200, 255) / 255, 1.0),
        scale=random.uniform(0.1, 0.35),
        position=Vec3(random.uniform(-180, 180), random.uniform(-180, 180), random.uniform(-180, 180)),
        unlit=True
    )

gunes_resim = resim_bul(['gunes', 'sun'])
sun = Entity(model='sphere', texture=gunes_resim if gunes_resim else None, color=color.white, scale=6, unlit=True)
Entity(parent=sun, model='sphere', color=color.rgba(255 / 255, 200 / 255, 50 / 255, 0.25), scale=1.18, unlit=True)

PointLight(parent=sun, position=(0, 0, 0), color=color.rgb(1.2, 1.1, 0.9), range=350, shadows=True)
AmbientLight(color=color.rgb(35 / 255, 35 / 255, 45 / 255))


def ciz_yorunge_cizgisi(mesafe):
    noktalar = []
    dilim = 120
    for i in range(dilim + 1):
        aci = math.radians(i * (360 / dilim))
        noktalar.append(Vec3(math.cos(aci) * mesafe, 0, math.sin(aci) * mesafe))
    Entity(model=Mesh(vertices=noktalar, mode='line', thickness=1.2), color=color.rgba(1, 1, 1, 0.25), unlit=True)


def olustur_saturn_halkasi(parent_gezegen):
    vertices, triangles, uvs = [], [], []
    dilimler, ic_cap, dis_cap = 60, 1.1, 2.2
    for i in range(dilimler + 1):
        aci = i * (2 * math.pi / dilimler)
        cos_a, sin_a = math.cos(aci), math.sin(aci)
        vertices.append(Vec3(cos_a * ic_cap, 0, sin_a * ic_cap))
        uvs.append((0, i / dilimler))
        vertices.append(Vec3(cos_a * dis_cap, 0, sin_a * dis_cap))
        uvs.append((1, i / dilimler))
    for i in range(dilimler):
        p1, p2, p3, p4 = i * 2, i * 2 + 1, (i + 1) * 2, (i + 1) * 2 + 1
        triangles.extend([(p1, p2, p3), (p2, p4, p3), (p3, p2, p1), (p3, p4, p2)])
    halka_mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, mode='triangle')
    halka_resmi = resim_bul(['saturn_halka', 'halka', 'saturn_ring', 'ring'])
    Entity(parent=parent_gezegen, model=halka_mesh, texture=halka_resmi if halka_resmi else None,
           color=color.white if halka_resmi else color.rgb(210 / 255, 190 / 255, 150 / 255), rotation_x=15, unlit=False,
           double_sided=True)


gezegen_verileri = {
    "merkur": {"ad": "Merkür", "tur": "Karasal", "mesafe": "9 Milyon km", "yas": "4.5 Milyar Yıl",
               "sicaklik": "Ort. 167°C", "ozellik": "Güneş'e en yakın\nve en küçük\ngezegendir."},
    "venus": {"ad": "Venüs", "tur": "Karasal", "mesafe": "13 Milyon km", "yas": "4.5 Milyar Yıl",
              "sicaklik": "Ort. 464°C", "ozellik": "Sıcaklığı en\nyüksek olan\ngezegendir."},
    "dunya": {"ad": "Dünya", "tur": "Karasal", "mesafe": "18 Milyon km", "yas": "4.54 Milyar Yıl",
              "sicaklik": "Ort. 15°C", "ozellik": "Yaşam barındıran\ntek evimizdir."},
    "mars": {"ad": "Mars", "tur": "Karasal", "mesafe": "23 Milyon km", "yas": "4.5 Milyar Yıl",
             "sicaklik": "Ort. -65°C", "ozellik": "Kızıl renkli\nkomşu gezegendir."},
    "jupiter": {"ad": "Jüpiter", "tur": "Gaz Devi", "mesafe": "31 Milyon km", "yas": "4.5 Milyar Yıl",
                "sicaklik": "Ort. -110°C", "ozellik": "En büyük gaz\ndevidir."},
    "saturn": {"ad": "Satürn", "tur": "Gaz Devi", "mesafe": "40 Milyon km", "yas": "4.5 Milyar Yıl",
               "sicaklik": "Ort. -140°C", "ozellik": "Muazzam halkalara\nsahiptir."},
    "uranus": {"ad": "Uranüs", "tur": "Buz Devi", "mesafe": "48 Milyon km", "yas": "4.5 Milyar Yıl",
               "sicaklik": "Ort. -195°C", "ozellik": "Yan yatmış\nbuz devidir."},
    "neptun": {"ad": "Neptün", "tur": "Buz Devi", "mesafe": "55 Milyon km", "yas": "4.5 Milyar Yıl",
               "sicaklik": "Ort. -200°C", "ozellik": "En uzak mavi\ngezegendir."},
    "pluton": {"ad": "Plüton", "tur": "Cüce Gezegen", "mesafe": "60 Milyon km", "yas": "4.5 Milyar Yıl",
               "sicaklik": "Ort. -230°C", "ozellik": "Kuiper Kuşağı'nda\nyer alan ünlü\ncüce gezegendir."}
}

# --- UI PANEL TASARIMLARI ---
sol_panel = Entity(parent=camera.ui, model='quad', color=color.rgb(45 / 255, 12 / 255, 18 / 255), scale=(0.36, 0.96),
                   position=(-0.7, 0))
Entity(parent=camera.ui, model='quad', color=color.rgb(130 / 255, 40 / 255, 55 / 255), scale=(0.365, 0.965),
       position=(-0.7, 0), z=0.01)
sol_panel.z = 0.02

Text(parent=camera.ui, text="-- KÜRESEL AJANS HABERLERİ --", scale=0.7, position=(-0.87, 0.43), origin=(-0.5, 0.5),
     color=color.rgb(255, 180, 180), z=-0.1)

haber_baslik_text = Text(parent=camera.ui, text="Bülten Hazırlanıyor...", scale=0.55, position=(-0.87, 0.33),
                         origin=(-0.5, 0.5), color=color.yellow, wordwrap=14, z=-0.1)
haber_detay_text = Text(
    parent=camera.ui,
    text="Haber akışı profesyonel\najans formatında başlatıldı.\nResmi bültenler, operasyon\nkodları ve adli gelişmeler\nburada canlı yayınlanacak.",
    scale=0.42,
    position=(-0.87, 0.22),
    origin=(-0.5, 0.5),
    color=color.white,
    wordwrap=16,
    line_height=1.2,
    z=-0.1
)

sag_panel = Entity(parent=camera.ui, model='quad', color=color.rgb(20 / 255, 25 / 255, 35 / 255), scale=(0.36, 0.96),
                   position=(0.7, 0))
Entity(parent=camera.ui, model='quad', color=color.rgb(70 / 255, 90 / 255, 130 / 255), scale=(0.365, 0.965),
       position=(0.7, 0), z=0.01)
sag_panel.z = 0.02

Text(parent=camera.ui, text="-- KONTROL PANELI --", scale=0.75, position=(0.53, 0.43), origin=(-0.5, 0.5),
     color=color.gold, z=-0.1)
tarih_text = Text(parent=camera.ui, text="Tarih: 2026 Yili - 1. Ay - 1. Gun", scale=0.48, position=(0.53, 0.37),
                  origin=(-0.5, 0.5), color=color.rgb(100 / 255, 220 / 255, 255 / 255), z=-0.1)

Text(parent=camera.ui, text="Zaman Hizi Carpani:", scale=0.45, position=(0.53, 0.31), origin=(-0.5, 0.5),
     color=color.light_gray, z=-0.1)
hiz_input = InputField(parent=camera.ui, default_value='100', scale=(0.28, 0.045), position=(0.7, 0.26), z=-0.1)

panel_baslik = Text(parent=camera.ui, text="Gezegen Secin", scale=0.75, position=(0.53, 0.19), origin=(-0.5, 0.5),
                    color=color.cyan, z=-0.1)
panel_detay = Text(
    parent=camera.ui,
    text="Simülasyona\nhoş geldiniz.\n\nİncelemek\nistediğiniz\ngezegene tıklayın.",
    scale=0.5,
    position=(0.53, 0.12),
    origin=(-0.5, 0.5),
    color=color.white,
    wordwrap=14,
    line_height=1.15,
    z=-0.1
)


def durdur_devam_et():
    global simulasyon_durdu
    simulasyon_durdu = not simulasyon_durdu
    if simulasyon_durdu:
        durdur_buton.text = "DEVAM ET"
        durdur_buton.color = color.rgb(46 / 255, 139 / 255, 87 / 255)
    else:
        durdur_buton.text = "DURDUR"
        durdur_buton.color = color.rgb(178 / 255, 34 / 255, 34 / 255)


durdur_buton = Button(parent=camera.ui, text='DURDUR', color=color.rgb(178 / 255, 34 / 255, 34 / 255),
                      scale=(0.28, 0.065), position=(0.7, -0.40), z=-0.1, on_click=durdur_devam_et)


def gezegene_tiklandi(isim):
    global simulasyon_durdu
    simulasyon_durdu = True
    durdur_buton.text = "DEVAM ET"
    durdur_buton.color = color.rgb(46 / 255, 139 / 255, 87 / 255)

    if isim in gezegen_verileri:
        veri = gezegen_verileri[isim]
        panel_baslik.text = f"{veri['ad'].upper()}"
        panel_detay.text = f"Tür: {veri['tur']}\nUzaklık: {veri['mesafe']}\nYaş: {veri['yas']}\nSıcaklık: {veri['sicaklik']}\n\n{veri['ozellik']}"


gezegen_listesi = [
    {"isim": "merkur", "olcek": 0.5, "mesafe": 9, "yorunge_hiz": 1.6, "donme_hiz": 15, "renk": color.gray},
    {"isim": "venus", "olcek": 0.8, "mesafe": 13, "yorunge_hiz": 1.2, "donme_hiz": -10,
     "renk": color.rgb(220 / 255, 180 / 255, 100 / 255)},
    {"isim": "dunya", "olcek": 1.0, "mesafe": 18, "yorunge_hiz": 1.0, "donme_hiz": 30, "renk": color.blue},
    {"isim": "mars", "olcek": 0.7, "mesafe": 23, "yorunge_hiz": 0.8, "donme_hiz": 28, "renk": color.red},
    {"isim": "jupiter", "olcek": 2.5, "mesafe": 31, "yorunge_hiz": 0.5, "donme_hiz": 50, "renk": color.orange},
    {"isim": "saturn", "olcek": 2.0, "mesafe": 40, "yorunge_hiz": 0.35, "donme_hiz": 45,
     "renk": color.rgb(240 / 255, 230 / 255, 140 / 255), "halka": True},
    {"isim": "uranus", "olcek": 1.4, "mesafe": 48, "yorunge_hiz": 0.25, "donme_hiz": -35, "renk": color.cyan},
    {"isim": "neptun", "olcek": 1.3, "mesafe": 55, "yorunge_hiz": 0.18, "donme_hiz": 35,
     "renk": color.rgb(60 / 255, 100 / 255, 230 / 255)},
    {"isim": "pluton", "olcek": 0.4, "mesafe": 60, "yorunge_hiz": 0.12, "donme_hiz": 20,
     "renk": color.rgb(180 / 255, 160 / 255, 140 / 255)},
]

gezegen_nesneleri = []
ay_nesnesi = None

for g in gezegen_listesi:
    ciz_yorunge_cizgisi(g["mesafe"])

    arama_isimleri = [g["isim"], 'pluto'] if g["isim"] == "pluton" else [g["isim"]]
    resim = resim_bul(arama_isimleri)

    gezegen = Entity(
        model='sphere',
        texture=resim if resim else None,
        color=color.white if resim else g["renk"],
        scale=g["olcek"],
        unlit=False,
        double_sided=True,
        collider='sphere'
    )
    gezegen.gezegen_adi = g["isim"]

    if g.get("halka"):
        olustur_saturn_halkasi(gezegen)

    if g["isim"] == "dunya":
        ay_resmi = resim_bul(['ay', 'moon'])
        ay = Entity(
            parent=gezegen,
            model='sphere',
            texture=ay_resmi if ay_resmi else None,
            color=color.white if ay_resmi else color.rgb(200 / 255, 200 / 255, 200 / 255),
            scale=0.3,
            unlit=False,
            double_sided=True
        )
        ay_nesnesi = {"entity": ay, "mesafe": 2.5, "yorunge_hiz": 3.0}

    gezegen_nesneleri.append({"entity": gezegen, "veri": g})

# --- KUİPER KUŞAĞI OLUŞTURMA ---
kuiper_taslari = []
silindir_model = Cylinder(resolution=8)

for _ in range(400):
    mesafe = random.uniform(63, 83)
    aci = random.uniform(0, 2 * math.pi)
    yukseklik = random.uniform(-1.8, 1.8)

    model_secimi = random.choice(['cube', 'sphere', silindir_model])

    boyut_x = random.uniform(0.12, 0.45)
    boyut_y = random.uniform(0.12, 0.45)
    boyut_z = random.uniform(0.12, 0.45)

    if random.random() < 0.5:
        r = random.uniform(0.6, 1.0)
        g = random.uniform(0.25, 0.65)
        b = random.uniform(0.0, 0.2)
        tas_rengi = color.rgb(r, g, b)
    else:
        gri_deger = random.uniform(0.15, 0.75)
        tas_rengi = color.rgb(gri_deger, gri_deger, gri_deger)

    tas = Entity(
        model=model_secimi,
        color=tas_rengi,
        scale=(boyut_x, boyut_y, boyut_z),
        position=Vec3(math.cos(aci) * mesafe, yukseklik, math.sin(aci) * mesafe),
        rotation=Vec3(random.randint(0, 360), random.randint(0, 360), random.randint(0, 360)),
        unlit=True
    )

    kuiper_taslari.append({
        "entity": tas,
        "mesafe": mesafe,
        "aci": aci,
        "hiz": random.uniform(0.04, 0.1)
    })


def input(key):
    if key == 'left mouse down':
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'gezegen_adi'):
            gezegene_tiklandi(mouse.hovered_entity.gezegen_adi)


EditorCamera()

t = 0


def update():
    global t, hiz_carpani, simulasyon_saniyesi, son_guncellenen_gun, mevcut_sky_durumu

    # --- KAMERA MESAFESİNE GÖRE DİNAMİK ARKA PLAN DEĞİŞİMİ ---
    kamera_mesafesi = camera.world_position.length()

    # Güneş sisteminden 16463.2 birim uzaklaşınca Samanyolu dokusu gelsin
    if kamera_mesafesi > 16463.2:
        if mevcut_sky_durumu != "samanyolu":
            mevcut_sky_durumu = "samanyolu"
            if samanyolu_resim:
                sky_entity.texture = samanyolu_resim
    else:
        if mevcut_sky_durumu != "uzay":
            mevcut_sky_durumu = "uzay"
            if uzay_resim:
                sky_entity.texture = uzay_resim
            else:
                sky_entity.color = color.rgb(5 / 255, 5 / 255, 10 / 255)

    try:
        hiz_carpani = float(hiz_input.text)
    except ValueError:
        pass

    if not simulasyon_durdu:
        delta_sim = time.dt * hiz_carpani
        t += delta_sim * 0.005
        simulasyon_saniyesi += delta_sim * 86400

        simulasyon_gunu = int(simulasyon_saniyesi // 86400)
        guncel_tarih = baslangic_tarihi + timedelta(seconds=simulasyon_saniyesi)
        tarih_text.text = f"Tarih: {guncel_tarih.year} Yili - {guncel_tarih.month}. Ay - {guncel_tarih.day}. Gun"

        if simulasyon_gunu != son_guncellenen_gun and simulasyon_gunu % 2 == 0:
            son_guncellenen_gun = simulasyon_gunu
            yeni_haber = rastgele_haber_uret()
            haber_baslik_text.text = yeni_haber["baslik"]
            haber_detay_text.text = yeni_haber["detay"]

        for item in gezegen_nesneleri:
            obj = item["entity"]
            data = item["veri"]
            aci = t * data["yorunge_hiz"]
            obj.x = math.cos(aci) * data["mesafe"]
            obj.z = math.sin(aci) * data["mesafe"]
            obj.rotation_y += time.dt * data["donme_hiz"] * (hiz_carpani / 100)

        for item in kuiper_taslari:
            item["aci"] += time.dt * item["hiz"] * 0.01 * (hiz_carpani / 100)
            x = math.cos(item["aci"]) * item["mesafe"]
            z = math.sin(item["aci"]) * item["mesafe"]
            item["entity"].x = x
            item["entity"].z = z
            item["entity"].rotation_x += time.dt * 5

        if ay_nesnesi:
            ay_obj = ay_nesnesi["entity"]
            ay_aci = t * ay_nesnesi["yorunge_hiz"]
            ay_obj.x = math.cos(ay_aci) * ay_nesnesi["mesafe"]
            ay_obj.z = math.sin(ay_aci) * ay_nesnesi["mesafe"]
            ay_obj.rotation_y += time.dt * 20


app.run()