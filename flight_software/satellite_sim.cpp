#include <iostream>
#include <string>
#include <random>
#include <chrono>
#include <thread>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

// Sensör verilerini JSON formatında üreten fonksiyon
std::string generate_telemetry() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_real_distribution<> voltage_dist(7.2, 8.4);
    std::uniform_real_distribution<> temp_dist(-50.0, 80.0);

    float voltage = voltage_dist(gen);
    float temperature = temp_dist(gen);

    return "{\"voltage\": " + std::to_string(voltage) + ", \"temperature\": " + std::to_string(temperature) + "}";
}

// Veriyi ağ üzerinden yer istasyonuna (FastAPI) gönderen fonksiyon
void send_data_to_server(const std::string& json_data) {
    int sock = 0;
    struct sockaddr_in serv_addr;

    // TCP Soketi oluştur
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        std::cerr << "[HATA] Soket oluşturulamadı." << std::endl;
        return;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8000); // Uvicorn/FastAPI portu

    // 127.0.0.1 (Localhost) adresine bağlan
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        std::cerr << "[HATA] Geçersiz IP adresi." << std::endl;
        return;
    }

    // Sunucuya bağlanmayı dene
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "[UYARI] Yer istasyonuna bağlanılamadı. FastAPI çalışıyor mu? Veri: " << json_data << std::endl;
        return;
    }

    // FastAPI'nin anlayabileceği standart HTTP POST isteğini manuel olarak hazırlıyoruz
    std::string http_request = 
        "POST /telemetry HTTP/1.1\r\n"
        "Host: 127.0.0.1:8000\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + std::to_string(json_data.length()) + "\r\n"
        "\r\n" + 
        json_data;

    // İsteği gönder ve soketi kapat
    send(sock, http_request.c_str(), http_request.length(), 0);
    std::cout << "[BAŞARILI] Telemetri gönderildi -> " << json_data << std::endl;
    
    close(sock);
}

int main() {
    std::cout << "[SISTEM] Uydu uçuş yazılımı (TCP Client) başlatıldı..." << std::endl;

    // Sonsuz döngü: 2 saniyede bir veri üret ve gönder
    while (true) {
        std::string telemetry_data = generate_telemetry();
        send_data_to_server(telemetry_data);
        
        std::this_thread::sleep_for(std::chrono::milliseconds(2000));
    }

    return 0;
}