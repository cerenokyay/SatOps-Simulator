import streamlit as st
import numpy as np
import onnxruntime as ort
import os
from PIL import Image

st.set_page_config(page_title="AI Uydu Analizi", page_icon="🧠", layout="wide")

st.title("🧠 Edge AI Destekli Uydu Görüntüsü Sınıflandırma")

# 1. Modeli Yükleme (ONNX Runtime ile)
# Model dosyasının yolu
#MODEL_PATH = "../ai_cnn_model.onnx"
MODEL_PATH = "/Users/cerenokyay/Desktop/SatOps-Simulator/ai_cnn_model.onnx"

@st.cache_resource
def load_onnx_model():
    if os.path.exists(MODEL_PATH):
        # Edge cihazlarda (CPU) yüksek hızda çalışması için Inception motorunu başlatıyoruz
        return ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
    else:
        return None

session = load_onnx_model()

if session is None:
    st.error(f"ONNX Model dosyası bulunamadı! Lütfen önce ana dizinde 'python ai_engine/train_cnn_onnx.py' komutunu çalıştırarak {MODEL_PATH} dosyasını oluşturun.")
else:
    # EuroSAT Sınıf İsimleri (CNN Eğitimimizde 10 sınıf vardı)
    classes = ['Tarımsal Alan', 'Orman', 'Otsu Bitki Örtüsü', 'Otoyol', 'Endüstriyel Alan', 
               'Otlak/Mera', 'Kalıcı Tarım Alanı', 'Yerleşim Yeri', 'Nehir', 'Deniz/Göl']
               
    st.subheader("Bölge Sınıflandırma Analizi")
    
    uploaded_file = st.file_uploader("Bir Uydu Görüntüsü Yükleyin (Tercihen 64x64 EuroSAT benzeri bir alan)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Orijinal Görüntü")
            # Resmi PIL ile aç ve göster
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, use_container_width=True)

        with col2:
            st.subheader("Yapay Zeka Analiz Raporu")
            
            with st.spinner("ONNX Runtime görüntüyü CNN ağından geçiriyor..."):
                
                # 2. Görüntüyü Modelin İstediği Formata (64x64 Tensör) Getirme
                # PyTorch'taki transform işleminin birebir aynısını yapmalıyız
                img_resized = image.resize((64, 64))
                img_array = np.array(img_resized).astype(np.float32)
                
                # Pikselleri 0-255 aralığından 0-1 aralığına çek (ToTensor)
                img_array /= 255.0
                
                # Renkleri Normalize et ((x - 0.5) / 0.5)
                img_array = (img_array - 0.5) / 0.5
                
                # HWC'den (Yükseklik, Genişlik, Renk) CHW'ye (Renk, Yükseklik, Genişlik) çevir
                img_array = np.transpose(img_array, (2, 0, 1))
                
                # Batch boyutunu ekle (1, 3, 64, 64)
                input_tensor = np.expand_dims(img_array, axis=0)

                # 3. ONNX Inference (Çıkarım) - Saniyeden daha kısa sürede
                input_name = session.get_inputs()[0].name
                outputs = session.run(None, {input_name: input_tensor})
                
                # Ham çıktıları (Logits) olasılıklara (Softmax) çevir
                logits = outputs[0][0]
                exp_preds = np.exp(logits - np.max(logits)) # Softmax stabilitesi için
                probabilities = exp_preds / np.sum(exp_preds)
                
                # En yüksek olasılığa sahip sınıfı bul
                predicted_class_index = np.argmax(probabilities)
                predicted_class = classes[predicted_class_index]
                confidence = probabilities[predicted_class_index] * 100

                # 4. Sonuçları Ekranda Gösterme
                st.success(f"**Bölge Tespiti:** {predicted_class}")
                st.info(f"**Yapay Zeka Emin Olma Oranı (Confidence):** %{confidence:.2f}")
                
                # Sadece görsel şölen için diğer sınıflara verilen olasılıkları gösterelim (İlk 3)
                st.write("---")
                st.markdown("**Diğer İhtimaller (Top 3):**")
                
                # İhtimalleri büyükten küçüğe sırala
                top3_indices = np.argsort(probabilities)[-3:][::-1]
                for idx in top3_indices:
                    st.write(f"- {classes[idx]}: %{probabilities[idx]*100:.1f}")