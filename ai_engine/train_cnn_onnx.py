import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import os

print("🛰️ [Edge AI] Gerçek Uydu Verisi (Sentinel-2 / EuroSAT) ile CNN Eğitimi Başlatılıyor...")

# 1. Gerçek Veri Setini (EuroSAT) İndirme ve Hazırlama
# Uydudan gelen görüntüleri modelin anlayacağı formata (Tensör) çeviriyoruz
transform = transforms.Compose([
    transforms.Resize((64, 64)), # EuroSAT resimleri orijinalde 64x64'tür
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) # Renkleri dengele
])

print("⬇️ Veri seti kontrol ediliyor (Eğer yoksa Avrupa Uzay Ajansı'ndan indirilecek, yaklaşık 2GB)...")
# dataset'i ./data klasörüne indirir
dataset = torchvision.datasets.EuroSAT(root='./data', download=True, transform=transform)

# Tüm veriyi beklememek için hızlı test adına ilk 2000 fotoğrafı alalım
# (Gerçek bir projede dataset'in tamamı kullanılır)
subset_indices = torch.randperm(len(dataset))[:2000]
subset = torch.utils.data.Subset(dataset, subset_indices)

trainloader = torch.utils.data.DataLoader(subset, batch_size=32, shuffle=True)
print(f"✅ Veri seti hazır! 10 farklı arazi sınıfında {len(subset)} adet gerçek uydu fotoğrafı ile eğitilecek.")

# Sınıf isimleri (EuroSAT için standarttır)
classes = ('AnnualCrop', 'Forest', 'HerbaceousVegetation', 'Highway', 'Industrial', 
           'Pasture', 'PermanentCrop', 'Residential', 'River', 'SeaLake')

# 2. Gerçek Görüntüler İçin Gelişmiş CNN Mimarisi
class SatelliteCNN(nn.Module):
    def __init__(self):
        super(SatelliteCNN, self).__init__()
        # Şekilleri ve kenarları öğrenen evrişim (Convolution) katmanları
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        
        # Sınıflandırma katmanı (64x64 resim 2 kez pool edilince 16x16'ya düşer)
        self.fc1 = nn.Linear(32 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, 10) # 10 farklı yeryüzü şekli

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1) # Düzleştir
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SatelliteCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. Model Eğitimi (Gerçek verilerle)
print("🧠 Eğitim başlıyor... (Bu işlem bilgisayarınızın hızına göre birkaç dakika sürebilir)")
epochs = 3 # Hızlı test için 3 tur (epoch) dönüyoruz

for epoch in range(epochs):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f"Epoch {epoch + 1}/{epochs} tamamlandı. Kayıp (Loss): {running_loss / len(trainloader):.3f}")

print("✅ Model gerçek verilerle başarıyla eğitildi!")

# 4. Uyduda Çalışması İçin ONNX Formatına Çevirme
model.eval()
dummy_input = torch.randn(1, 3, 64, 64) # Sisteme 64x64'lük bir resim gireceğini belirtiyoruz
onnx_path = "../ai_cnn_model.onnx"

torch.onnx.export(
    model, dummy_input, onnx_path, 
    export_params=True, opset_version=18, do_constant_folding=True,
    input_names=['input_image'], output_names=['classification_output'],
    dynamic_axes={'input_image': {0: 'batch_size'}, 'classification_output': {0: 'batch_size'}}
)

print(f"🚀 [Edge AI] Model başarıyla ONNX formatında derlendi: {os.path.abspath(onnx_path)}")