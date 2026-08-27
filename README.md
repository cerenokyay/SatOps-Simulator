# 🛰️ SatOps Ground Station Complex

Bu proje, uzay operasyonları ve telemetri yönetimi için geliştirilmiş, uçtan uca veri akışı ve yapay zeka çıkarımı (inference) yapabilen modüler bir yer istasyonu simülasyonudur. Sistem, düşük seviyeli donanım haberleşmesinden yüksek seviyeli makine öğrenmesi analizlerine kadar geniş bir yelpazeyi kapsar.

## 🏗️ Sistem Mimarisi (V2.0)

Proje iki ana fazdan ve birbirine entegre üç sistemden oluşmaktadır:

1. **Uçuş Yazılımı ve TCP İletişimi (C++ & FastAPI)**
   * C++ ile yazılmış gömülü sistem simülatörü, rastgele sensör (voltaj/sıcaklık) verileri üretir.
   * Veriler TCP Soketleri üzerinden asenkron FastAPI (Uvicorn) sunucusuna iletilir.
   * Gelen telemetri paketleri doğrulanarak SQLite veritabanına kalıcı olarak yazılır.

2. **Canlı Yörünge Takibi (REST API & JS)**
   * Açık kaynaklı ISS (Uluslararası Uzay İstasyonu) API'leri kullanılarak anlık koordinat ve hız verileri çekilir.
   * Leaflet.js ve Folium entegrasyonu ile Streamlit üzerinde ekran kararması (flicker) yaşanmadan kesintisiz yörünge takibi sağlanır.

3. **Yapay Zeka Görüntü Analizi (Yakında)**
   * Uydu görüntüleri üzerinde scikit-learn ve makine öğrenmesi modelleri koşularak bulut yoğunluğu ve çevresel analiz (inference) yapılır.

## 🚀 Teknolojiler
* **Backend:** Python 3.13, FastAPI, Uvicorn, SQLAlchemy, SQLite
* **Frontend:** Streamlit, Folium, Leaflet.js
* **Simülasyon:** C++17 (Socket Programming)
* **Yapay Zeka (AI/ML):** scikit-learn, ONNX Runtime (Geliştirme Aşamasında)



## 🔬 Örnek Olay İncelemesi (Case Study): Görüntü İşlemede Sınır Durumlar (Edge Cases)

**Test Senaryosu:** Karadeniz Üzerindeki Fitoplankton Patlamaları (Phytoplankton Blooms)
**Kullanılan Model:** RGB Piksel Tabanlı Lojistik Regresyon

Sisteme Karadeniz'in turkuaz renkli fitoplankton patlamalarını içeren bir uydu görüntüsü yüklendiğinde, model su alanının büyük bir bölümünü (%56.5) **"Bitki Örtüsü"** olarak sınıflandırmıştır. 

**Neden Böyle Oldu?**
Fitoplankton patlamaları, piksel bazında çok yüksek "Yeşil (G)" yoğunluğuna sahiptir. Mevcut Lojistik Regresyon modelimiz piksellerin geometrik şekline, dokusuna veya bağlamına (spatial context) değil, yalnızca bağımsız RGB renk uzayına bakarak karar vermektedir. Model; yeşil tonu algıladığında, "Suyu yalnızca koyu mavi (düşük R, düşük G, yüksek B) olarak öğrenmiştim, bu bölgede yeşil yoğunluğu çok yüksek, dolayısıyla burası bitki örtüsüdür" mantığıyla hatalı bir çıkarım yapmıştır.

**Mühendislik Çıkarımı ve Çözüm Önerisi:**
Bu durum, bağımsız RGB pikselleriyle eğitilen temel sınıflandırma algoritmalarının limitlerini kanıtlayan muazzam bir "Edge Case" (uç durum) örneğidir. Gerçek uydu ve yer istasyonu operasyonlarında bu yanılgıyı ortadan kaldırmak için:
1. **Sensör Geliştirmesi:** Standart RGB kameralar yerine Yakın Kızılötesi (NIR - Near Infrared) bantlarına sahip multispektral sensörler kullanılmalıdır.
2. **Mimari Geliştirme:** Pikselleri tekil olarak değil, komşuluk ilişkileri ve şekilsel bütünlüğüyle (spatial coherence) analiz edebilmek için CNN (Evrişimli Sinir Ağları) gibi Derin Öğrenme mimarilerine geçiş yapılmalıdır.