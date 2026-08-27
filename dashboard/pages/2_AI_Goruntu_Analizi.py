import streamlit as st
import numpy as np
import joblib
import os
from PIL import Image

st.set_page_config(page_title="AI Uydu Analizi", page_icon="🧠", layout="wide")

st.title("🧠 Yapay Zeka Destekli Uydu Görüntüsü Analizi")
st.markdown("Eğitilmiş modelimiz ile uydu fotoğraflarını yükleyin, AI tüm pikselleri tarayarak bölgenin yeryüzü şekillerini oranlasın.")

MODEL_PATH = "../ai_model.pkl" 

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return None

model = load_model()

if model is None:
    st.error(f"Model dosyası bulunamadı! Lütfen önce {MODEL_PATH} dosyasını oluşturun.")
else:
    # 1. Dosya Yükleme Alanı
    uploaded_file = st.file_uploader("Bir Uydu Görüntüsü Yükleyin (JPG/PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Orijinal Görüntü")
            # Resmi PIL ile aç ve göster
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("Yapay Zeka Analiz Raporu")
            
            with st.spinner("AI pikselleri tarıyor ve sınıflandırıyor..."):
                # Resmi numpy dizisine (piksellere) çevir
                img_array = np.array(image)
                
                # Resim çok büyükse (örn 4K), modelin kilitlenmemesi için yeniden boyutlandır
                if img_array.shape[0] > 300 or img_array.shape[1] > 300:
                    image_small = image.resize((300, 300))
                    img_array = np.array(image_small)

                # Şeffaflık (Alpha) kanalı varsa at (Sadece RGB lazım)
                if img_array.shape[2] == 4:
                    img_array = img_array[:, :, :3]

                # (Genişlik, Yükseklik, 3) formatındaki resmi (Toplam Piksel Sayısı, 3) formatına düzleştir
                pixels = img_array.reshape(-1, 3)
                
                # Modeli çalıştır (Tüm pikseller için aynı anda tahmin yap)
                predictions = model.predict(pixels)
                
                # Tahminlerin sayısını bul (Hangi sınıftan kaç piksel var?)
                unique, counts = np.unique(predictions, return_counts=True)
                total_pixels = len(predictions)
                
                # Sonuçları hesapla ve ekrana yazdır
                class_names = {0: "☁️ Bulut", 1: "💧 Su Kaynağı", 2: "🌳 Bitki Örtüsü", 3: "🟤 Toprak/Çorak Alan"}
                
                for val, count in zip(unique, counts):
                    percentage = (count / total_pixels) * 100
                    st.metric(label=class_names.get(val, "Bilinmeyen"), value=f"%{percentage:.1f}")

        st.success("✅ Görüntü analizi tamamlandı.")
        
    st.divider()
    st.caption("Not: Bu model prototip aşamasındadır. Yüksek doğruluk için binlerce uydu görüntüsüyle eğitilmiş Derin Öğrenme (CNN) modelleri önerilir.")