# SatOps Simulator 🛰️

End-to-end satellite flight software simulation and ground station telemetry dashboard.

## Proje Mimarisi

Bu proje üç ana bileşenden oluşmaktadır:
1. **Flight Software (C++):** Uydunun sensör verilerini (batarya voltajı, güneş paneli sıcaklığı) simüle eder ve TCP üzerinden yer istasyonuna gönderir.
2. **Ground Station (Python / FastAPI):** Uydudan gelen telemetri verilerini dinler, doğrular ve SQLite veritabanına kaydeder.
3. **Dashboard (Python / Streamlit):** Gerçek zamanlı verileri görselleştiren, anormallikleri takip eden kontrol paneli.

## Kurulum ve Çalıştırma

### Gereksinimler
- C++17 destekleyen bir derleyici (g++)
- Python 3.9+

### Adımlar (Çok Yakında)
- Proje çalıştırma talimatları buraya eklenecektir.