import streamlit as st

st.set_page_config(page_title="AI Uydu Analizi", page_icon="🧠", layout="wide")

st.title("🧠 Yapay Zeka Destekli Uydu Görüntüsü Analizi")
st.markdown("NASA/ESA API'lerinden alınan güncel uydu görüntüleri üzerinde makine öğrenmesi modelleriyle analiz yapılır.")

# Kullanıcıdan lokasyon ve analiz tipi alma
col1, col2 = st.columns(2)
with col1:
    location = st.selectbox("Analiz Edilecek Bölge", ["İzmir, Türkiye", "Manisa, Türkiye", "Amazon Ormanları, Brezilya"])
with col2:
    model_type = st.selectbox("Uygulanacak AI Modeli", ["Bulut Yoğunluğu Tespiti (Lojistik Regresyon)", "Su Kaynağı Analizi", "Bitki Örtüsü Sınıflandırma"])

st.button("Görüntüyü Çek ve Modeli Çalıştır")

st.info("API bağlantıları ve çıkarım (inference) motoru bekleniyor... İlerleyen aşamada model sonuçları burada görselleştirilecektir.")

# Şimdilik yer tutucu olarak boş bir alan
st.divider()
st.caption("AI Çıkarım Sonuçları (Yakında)")