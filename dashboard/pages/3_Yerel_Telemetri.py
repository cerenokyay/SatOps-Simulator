import streamlit as st
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="Misyon Analizi", page_icon="📈", layout="wide")

st.title("📈 Dinamik Uçuş Verisi (Playback) Analizi")
st.markdown("Farklı uydu misyonlarına ait telemetri dosyalarını (CSV) yükleyerek sistem performansını ve donanım eğrilerini analiz edin.")

# 1. Dosya Yükleme Alanı (File Uploader)
uploaded_file = st.file_uploader("Geçmiş Misyon Verisini (CSV) Yükle", type=["csv"])

if uploaded_file is not None:
    try:
        # 2. Yüklenen dosyayı Pandas ile belleğe al
        df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ Dosya başarıyla yüklendi! Toplam {len(df)} satır veri analiz ediliyor.")
        st.divider()
        
        # 3. Verilerin Genel Özeti (KPI Kartları)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ortalama Voltaj", f"{df['voltage'].mean():.2f} V")
        with col2:
            st.metric("Maksimum Sıcaklık", f"{df['temperature'].max():.2f} °C")
        with col3:
            st.metric("Minimum Sıcaklık", f"{df['temperature'].min():.2f} °C")
            
        st.write("---")
        
        # 4. Dinamik Grafikler
        chart1, chart2 = st.columns(2)
        with chart1:
            st.subheader("Batarya Deşarj Eğrisi")
            st.line_chart(df, x="timestamp", y="voltage", color="#FF4B4B")
            
        with chart2:
            st.subheader("Termal Dalgalanma")
            st.line_chart(df, x="timestamp", y="temperature", color="#0068C9")
            
        # 5. Ham Veri Tablosu (Opsiyonel inceleme için)
        with st.expander("Ham Verileri Görüntüle"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Dosya okunurken bir hata oluştu: {e}. Lütfen doğru formatta bir CSV yüklediğinizden emin olun.")
else:
    st.info("👆 Lütfen analiz etmek istediğiniz bir telemetri (.csv) dosyasını yukarıdan sisteme yükleyin.")