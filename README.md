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