import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib
import os

print("[AI Engine] Uydu görüntüsü analiz modeli eğitimi başlatılıyor...")

# 1. Eğitim Verisini (Dataset) Hazırlama
# Pratikte bu veriler on binlerce gerçek uydu fotoğrafından elde edilir.
# Şimdilik modelin mantığını kurmak için (RGB renk kodları) temsili veriler kullanıyoruz.

# X (Özellikler): Piksellerin R, G, B değerleri (0-255 arası)
X_train = np.array([
    [240, 240, 240], [255, 255, 255], [200, 200, 200], # Parlak beyaz/gri -> Bulut
    [10, 20, 150], [5, 10, 200], [0, 50, 180],         # Yoğun mavi -> Su
    [34, 139, 34], [0, 100, 0], [107, 142, 35],        # Yeşil tonları -> Bitki Örtüsü
    [139, 69, 19], [160, 82, 45], [210, 180, 140]      # Kahverengi tonları -> Toprak
])

# Y (Etiketler): Hangi pikselin neye karşılık geldiği
# 0: Bulut, 1: Su, 2: Bitki Örtüsü, 3: Toprak
y_train = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])

# 2. Modeli Tanımlama ve Eğitme
print("[AI Engine] Lojistik Regresyon modeli eğitiliyor...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 3. Modeli Kaydetme
# Eğitilmiş modeli Streamlit'in kullanabilmesi için bir dosyaya kaydediyoruz.
model_path = "ai_model.pkl"
joblib.dump(model, model_path)

print(f"[AI Engine] Model başarıyla eğitildi ve kaydedildi: {os.path.abspath(model_path)}")