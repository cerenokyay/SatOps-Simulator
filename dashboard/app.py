import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

# Sayfa ayarları (Tam ekran genişliğinde)
st.set_page_config(page_title="SatOps Dashboard", page_icon="🛰️", layout="wide")

st.title("🛰️ SatOps Telemetry Dashboard")
st.markdown("Uydudan gelen gerçek zamanlı sağlık ve durum verileri.")

# Veritabanına bağlantı kuralım
# Not: dashboard klasöründen ground_station içindeki db'ye erişmek için doğru yolu verdik
DATABASE_URL = "sqlite:///../ground_station/telemetry.db"
engine = create_engine(DATABASE_URL)

# Veritabanından son 50 veriyi çeken fonksiyon
def get_data():
    query = "SELECT * FROM telemetry ORDER BY id DESC LIMIT 50"
    try:
        df = pd.read_sql(query, engine)
        df = df.sort_values(by="id") # Grafikte soldan sağa akması için tekrar eskiye->yeniye sırala
        return df
    except Exception as e:
        return pd.DataFrame()

# Sayfanın düzenini oluştur (2 kolon)
col1, col2 = st.columns(2)

# Sürekli güncellenen bir alan (placeholder) oluştur
placeholder = st.empty()

# Sonsuz döngü ile sayfayı otomatik yenile
while True:
    df = get_data()
    
    if not df.empty:
        # En güncel voltaj ve sıcaklık değerini al
        current_voltage = df.iloc[-1]['voltage']
        current_temp = df.iloc[-1]['temperature']
        
        with placeholder.container():
            # Üstteki metrik (KPI) kartları
            kpi1, kpi2 = st.columns(2)
            kpi1.metric(label="Anlık Batarya Voltajı (V)", value=f"{current_voltage:.2f}")
            kpi2.metric(label="Anlık Güneş Paneli Sıcaklığı (°C)", value=f"{current_temp:.2f}")
            
            # Alt taraftaki grafikler
            chart1, chart2 = st.columns(2)
            with chart1:
                st.subheader("Batarya Eğilimi")
                st.line_chart(df, x="timestamp", y="voltage", color="#FF4B4B")
                
            with chart2:
                st.subheader("Sıcaklık Eğilimi")
                st.line_chart(df, x="timestamp", y="temperature", color="#0068C9")
                
    else:
        st.warning("Henüz veritabanında veri yok. C++ simülatörünün çalıştığından emin olun.")
        
    # Her 2 saniyede bir ekranı güncelle
    time.sleep(2)