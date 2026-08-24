import streamlit as st

st.set_page_config(page_title="SatOps Ground Station", page_icon="📡", layout="wide")

st.title("📡 SatOps Yer İstasyonu Kompleksi")
st.markdown("""
Bu kontrol paneli iki ana operasyon modülünden oluşmaktadır:

*   👈 **Sol menüden gitmek istediğiniz modülü seçin:**
    *   **1. ISS Telemetri:** Uluslararası Uzay İstasyonu'nun gerçek zamanlı konum ve hız verileri.
    *   **2. AI Görüntü Analizi:** Açık kaynaklı uydu görüntülerinin çekilmesi ve optimize edilmiş makine öğrenmesi modelleriyle (ONNX vb.) gerçek zamanlı yeryüzü analizlerinin (çıkarım/inference) yapılması.
""")