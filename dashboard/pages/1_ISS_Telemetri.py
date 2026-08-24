import streamlit as st
import streamlit.components.v1 as components

# Sayfa Ayarları
st.set_page_config(page_title="ISS Telemetri", page_icon="🌍", layout="wide")

st.title("🌍 Uluslararası Uzay İstasyonu (ISS) Canlı Takip")
st.markdown("Bu modül, ekran kararmasını önlemek için doğrudan tarayıcı üzerinde (Client-Side) çalışan kesintisiz bir izleme haritası kullanır.")
st.divider()

# Ekran kararmasını önleyen özel HTML/JS Harita Modülü
# Uydunun hareketini Streamlit'i yenilemeden, tarayıcı içinde canlı yapar.
map_html = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map { height: 550px; width: 100%; border-radius: 10px; border: 2px solid #333; }
        body { margin: 0; padding: 0; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Haritayı dünya merkezli başlat
        var map = L.map('map').setView([0, 0], 3);
        
        // Açık kaynaklı harita katmanını ekle
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 10,
            attribution: '© OpenStreetMap'
        }).addTo(map);

        // Özel Uydu (ISS) İkonu tanımla
        var issIcon = L.icon({
            iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/d/d0/International_Space_Station.svg',
            iconSize: [60, 60],
            iconAnchor: [30, 30]
        });

        // İkonu haritaya ekle (başlangıç konumu 0,0)
        var issMarker = L.marker([0, 0], {icon: issIcon}).addTo(map);
        
        // Uydunun geçtiği yerlere kırmızı bir çizgi (iz) bırakmak için
        var path = L.polyline([], {color: 'red', weight: 2}).addTo(map);

        // API'den veriyi çekip sadece ikonu hareket ettiren fonksiyon
        function updateLocation() {
            // Güvenli (HTTPS) ve hızlı bir alternatif ISS API'si
            fetch('https://api.wheretheiss.at/v1/satellites/25544')
                .then(response => response.json())
                .then(data => {
                    var lat = parseFloat(data.latitude);
                    var lon = parseFloat(data.longitude);
                    
                    // İkonu yeni konuma kaydır
                    issMarker.setLatLng([lat, lon]);
                    
                    // Haritanın merkezini uyduya göre yavaşça kaydır
                    map.panTo([lat, lon], {animate: true, duration: 1.0});
                    
                    // Geçtiği yolu kırmızı çizgiye ekle
                    path.addLatLng([lat, lon]);
                })
                .catch(err => console.error("API Hatası:", err));
        }

        // Sayfa açıldığında ilk veriyi çek
        updateLocation();
        
        // Her 2 saniyede bir ekranı hiç yenilemeden sadece fonksiyonu çalıştır
        setInterval(updateLocation, 2000);
    </script>
</body>
</html>
"""

# HTML bloğunu Streamlit içine göm
components.html(map_html, height=600)