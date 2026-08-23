#include <iostream>
#include <string>
#include <random>
#include <chrono>
#include <thread>

// Sensör verilerini JSON formatında üreten fonksiyon
std::string generate_telemetry() {
    // Rastgele sayı üreticileri (Mersenne Twister)
    static std::random_device rd;
    static std::mt19937 gen(rd());
    
    // Sensör sınır değerleri
    std::uniform_real_distribution<> voltage_dist(7.2, 8.4); // Batarya (V)
    std::uniform_real_distribution<> temp_dist(-50.0, 80.0); // Sıcaklık (C)

    float voltage = voltage_dist(gen);
    float temperature = temp_dist(gen);

    // Basit bir JSON formatında paketleme
    std::string payload = "{\"voltage\": " + std::to_string(voltage) + 
                          ", \"temperature\": " + std::to_string(temperature) + "}";
    
    return payload;
}

int main() {
    std::cout << "[SISTEM] Uydu uçuş yazılımı başlatıldı..." << std::endl;
    std::cout << "[SISTEM] Telemetri verileri üretiliyor.\n" << std::endl;

    // Sonsuz döngü: Saniyede 1 kez veri üretir
    while (true) {
        std::string telemetry_data = generate_telemetry();
        
        // Şimdilik sadece ekrana yazdırıyoruz, daha sonra buraya TCP gönderimi eklenecek
        std::cout << "[GÖNDERİLECEK PAKET] -> " << telemetry_data << std::endl;

        // 1 saniye bekle (1000 milisaniye)
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }

    return 0;
}