import os
import time
import random
import matplotlib.pyplot as plt
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


# ====================== Fungsi-Fungsi Terkait ==========================

# Fungsi yang mencari semua kemungkinan solusi yang bisa dihasilkan dari permutasi N buah queen ke dalam papan pada baris dan kolom yang berbeda
def permutasi(jumlah_queen, jumlah_kolom):
    # Simpan semua kemungkinan hasil di dalam sebuah array
    semua_kemungkinan = []
    kolom_dipakai = [False] * jumlah_kolom
    posisi = [-1] * jumlah_queen

    # Fungsi Rekursif Pembantu untuk menempatkan Queen di baris
    def generate(baris):
        # Basis : semua queen sudah diposisikan
        if baris == jumlah_queen:

            papan_temp = [["." for _ in range(jumlah_kolom)] for _ in range(jumlah_baris)]
            for r in range(jumlah_queen):
                papan_temp[r][posisi[r]] = "#"

            semua_kemungkinan.append(papan_temp)
            return
            
        # Rekursif
        for kolom in range(jumlah_kolom):
            if not kolom_dipakai[kolom]:
                kolom_dipakai[kolom] = True
                posisi[baris] = kolom
                generate(baris + 1)
                kolom_dipakai[kolom] = False
            
    generate(0)
    return semua_kemungkinan

# Fungsi Boolean untuk mengecek posisi tertentu pada papan aman untuk menempatkan queen
def cek_posisi_aman(baris, kolom, papan_temp, papan_warna):
    current = papan_warna[baris][kolom]

    # cek apakah ada di warna / baris / kolom yang sama
    for i in range (jumlah_baris):
        for j in range (jumlah_kolom):
            if papan_temp[i][j] == "#":
                # Skip posisi saat ini
                if i == baris and j == kolom:
                    continue

                # Cek warna
                if papan_warna[i][j] == current:
                    return False

                # Cek baris
                if i == baris :
                    return False
                
                # Cek kolom
                if j == kolom:
                    return False

    # cek apakah bersebelahan
    for jarak_baris in [-1, 0, 1]:
        for jarak_kolom in [-1, 0, 1]:
            # Lewati current kotak
            if jarak_baris == 0 and jarak_kolom == 0: 
                continue 

            baris_tetangga, kolom_tetangga = baris + jarak_baris, kolom + jarak_kolom
            if 0 <= baris_tetangga < jumlah_baris and 0 <= kolom_tetangga < jumlah_kolom:
                if papan_temp[baris_tetangga][kolom_tetangga] == "#":
                    return False
        
    # Selain kondisi syarat:
    return True

# Fungsi Boolean untuk mengecek apakah sebuah papan valid sesuai syarat permainan
def cek_kemungkinan_aman(kemungkinan, jumlah_baris, jumlah_kolom, papan_warna):
    for baris in range(jumlah_baris):
        for kolom in range(jumlah_kolom):
            if kemungkinan[baris][kolom] == "#":
                if not cek_posisi_aman(baris, kolom, kemungkinan, papan_warna):
                    return False
    
    return True          

# Fungsi yang mengambil solusi valid pertama dari semua kemungkinan solusi
def temukan_kemungkinan_aman(semua_kemungkinan, papan_warna, jumlah_baris, jumlah_kolom):
    total = len(semua_kemungkinan)

    for idx, kemungkinan in enumerate(semua_kemungkinan):

        # Live Update
        if idx % max(1, total // 20) == 0:  # update tiap 5%
            persen = (idx / total) * 100
            print(Fore.YELLOW + f"[Progress] {persen:.1f}%  ({idx}/{total}) kemungkinan dicek")
            show_papan(kemungkinan, jumlah_baris, jumlah_kolom)

        # Cari kemungkinan hasil yang aman
        if cek_kemungkinan_aman(kemungkinan, jumlah_baris, jumlah_kolom, papan_warna):
            print(Fore.GREEN + f"\nSolusi ditemukan pada kemungkinan ke-{idx}")
            return kemungkinan

    # Jika tidak ditemukan solusi
    print(Fore.RED + "Tidak ditemukan kemungkinan solusi")
    return None
        

# Fungsi Helper
# Load File txt papan
def load_file():
    folder = "../test/"
    # Input nama file untuk papan
    file_name = input("Masukkan nama file (format .txt) : ")
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    
    full_path = os.path.join(folder, file_name)

    while not os.path.exists(full_path):
        print(Fore.YELLOW + f"File '{file_name}' tidak ditemukan di folder test ini.")
        file_name = input("Masukkan nama file kembali: ")
        full_path = os.path.join(folder, file_name)


    with open(full_path, 'r') as file:
        # Mengambil matriks papan warna dari file
        papan_warna = [list(line.strip()) for line in file]

        # Menyimpan set warna yang ada
        set_warna = set()
        for baris in papan_warna:
            for elemen in baris:
                set_warna.add(elemen)
        
    return papan_warna, set_warna

def save_file(papan_final, kasus, durasi, jumlah_queen):
    folder = "../test/"
    file_name = input("Masukkan nama file yang akan disimpan : ")

    # Validasi File txt
    # Tambahkan .txt otomatis jika user lupa mengetiknya
    if not file_name.endswith(".txt"):
        file_name += ".txt"
    
    full_path = os.path.join(folder, file_name)

    # Validasi Jika File memiliki nama serupa
    while os.path.exists(full_path):
        print(Fore.YELLOW + f"Peringatan: File '{file_name}' sudah ada!")
        pilihan = input(Fore.YELLOW + "Apakah ingin menimpa (overwrite) file tersebut? (Ya/Tidak): ").capitalize()
        
        if pilihan == "Ya":
            break # Keluar dari loop while dan lanjut simpan (overwrite)
        else:
            # Jika tidak ingin menimpa, minta nama file baru
            file_name = input("Masukkan nama file baru: ")
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            full_path = os.path.join(folder, file_name)
            

    # Validasi File Gambar
    # Ambil tanpa ".txt"
    base_name = os.path.splitext(full_path)[0]
    image_file = base_name + ".png"
    path_image = os.path.join(folder, image_file)
        
    # Simpan Gambar
    plt.savefig(image_file, bbox_inches="tight", dpi=300)


    with open(full_path, 'w') as f_out:
        f_out.write("================================================\n")
        f_out.write("========= Solusi Games Queens LinkedIn =========\n")
        f_out.write("================================================\n")

        f_out.write(f"{jumlah_queen} Queens berhasil diposisikan\n\n")
        f_out.write("Hasil Penempatan Queens:\n")
        for baris in papan_final:
            # Menggabungkan list menjadi string lalu menambah enter (\n)
            baris_string = "".join(baris) + "\n"
            f_out.write(baris_string)
        
        f_out.write(f"\nDurasi pencarian : {durasi*100:.2f} ms\n")
        f_out.write(f"Banyak kasus yang ditinjau : {kasus} kasus")

    show_nama_file = os.path.splitext(file_name)[0]
    print(f"\nHasil penempatan Queen pada papan berhasil disimpan pada file : \n")
    print(Fore.GREEN + f"{show_nama_file}.txt dan visualisasi pada {show_nama_file}.png\n")

# Tampilan CLI Menarik
# Menampilkan Papan di CLI
def show_papan(papan, jumlah_baris, jumlah_kolom):
    # Garis pembatas horizontal
    garis_horizontal = "  +" + "---+" * jumlah_kolom

    # Cetak nomor kolom
    print("   ", end="")
    for c in range(jumlah_kolom):
        print(f" {c}  ", end="")
    print()

    # Mapping warna random
    pilihan_warna = [
        Back.RED,
        Back.GREEN,
        Back.YELLOW,
        Back.BLUE,
        Back.MAGENTA,
        Back.CYAN,
    ]

    warna_map = {}
    for baris in papan:
        for cell in baris:
            if cell != "#" and cell not in warna_map:
                warna_map[cell] = random.choice(pilihan_warna)

    for i, baris_data in enumerate(papan):
        print(Style.BRIGHT + garis_horizontal)
        # Cetak nomor baris di samping
        print(f"{i} |", end="") 
        for cell in baris_data:
            # Jika cell adalah Queen, beri spasi ekstra agar menonjol
            if cell == "#":
                print(Back.WHITE + Fore.YELLOW + Style.BRIGHT + " # ", Fore.RESET + Style.BRIGHT + "|", sep="", end="")
            else:
                style = warna_map[cell]
                print(style + warna_map[cell] + f" {cell} " + Back.RESET + Style.BRIGHT + "|", end="")
        print()
    print(garis_horizontal)

# Membuat gambar dari papan
def papan_to_image(papan, papan_warna):
    n_baris = len(papan)
    n_kolom = len(papan[0])

    # map warna huruf -> warna random
    unik = sorted(set(c for row in papan_warna for c in row))
    cmap = {u:(random.random(),random.random(),random.random()) for u in unik}

    fig, ax = plt.subplots()

    for i in range(n_baris):
        for j in range(n_kolom):
            rect = plt.Rectangle(
                (j, n_baris-i-1),
                1,1,
                facecolor=cmap[papan_warna[i][j]],
                edgecolor="black"
            )
            ax.add_patch(rect)

            if papan[i][j] == "#":
                ax.text(j+0.5, n_baris-i-0.5, "♛", 
                        ha="center", va="center", fontsize=18)

    ax.set_xlim(0, n_kolom)
    ax.set_ylim(0, n_baris)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()

# Closing Statement Program saar Program Berakhir
def closing_statement():
    print(Fore.YELLOW + "======================================================================")
    print(Fore.YELLOW + "========== " + Fore.RESET + "👑 Terima kasih telah bermain Queens LinkedIn 👑" + Fore.YELLOW + " ==========")
    print(Fore.YELLOW + "======================================================================")

# =========================== Program Utama =================================
# Opening Statement Program
print(Fore.YELLOW + "==================================================================")
print(Fore.YELLOW + "=========== " + Fore.RESET + "👑 Selamat Datang di Queens LinkedIn 👑" + Fore.YELLOW + " ==============")
print(Fore.YELLOW + "==================================================================")

# 1. Input nama file papan
papan_warna, set_warna = load_file()

# 2. Tampilkan papan yang akan disolve
jumlah_baris = len(papan_warna)
jumlah_kolom = len(papan_warna[0])

print(Fore.YELLOW + "\n======== Papan Warna Queens ========")
show_papan(papan_warna, jumlah_baris, jumlah_kolom)

print("Jumlah baris : ", jumlah_baris)
print("Jumlah kolom : ", jumlah_kolom)

# 3. Jalankan Program Utama : Pencarian dan Pemosisian Queen
opsi_lanjutan = input("Lanjutkan proses penempatan Queen? (Ya/Tidak) : ")
while opsi_lanjutan != "Ya" and opsi_lanjutan != "Tidak":
    print(Fore.YELLOW + "Pilihan tidak valid, ulangi masukkan Anda!")
    opsi_lanjutan = input("Lanjutkan proses penempatan Queen? (Ya/Tidak) : ")

if opsi_lanjutan == "Tidak":
    closing_statement()

else:
    print("\nMencari posisi queen yang sesuai...")

    # Mulai waktu pencarian
    mulai = time.time()
    
    # Proses Iterasi Pencarian 
    jumlah_queen = len(set_warna) # Jumlah queen = jumlah anggota set warna
    semua_kemungkinan = permutasi(jumlah_queen, jumlah_kolom) 

    # Hitung jumlah kasus yang dicek
    kasus = len(semua_kemungkinan)

    hasil = temukan_kemungkinan_aman(semua_kemungkinan, papan_warna, jumlah_baris, jumlah_kolom)

    # catat durasi pencarian
    selesai = time.time()
    durasi = selesai - mulai

    if hasil == None:
        print(Fore.RED + "Papan Queens tidak dapat diselesaikan")  

    else:
        print(Fore.GREEN + "Queen sudah berhasil diposisikan")

        # Salin hasil penempatan queen ke papan warna
        papan_final = []
        for i in range(jumlah_baris):
            baris_papan = []
            for j in range(jumlah_kolom):
                if hasil[i][j] == "#":
                    baris_papan.append("#")
                else:
                    baris_papan.append(papan_warna[i][j])
            papan_final.append(baris_papan)

        # Hasil akhir
        print(Fore.YELLOW + "\n=========================================================")
        print(Fore.YELLOW + "===== Hasil Akhir Penempatan Queen pada Papan Warna =====")
        print(Fore.YELLOW + "=========================================================")

        # Menampilkan Hasil Penempatan Queens
        show_papan(papan_final, jumlah_baris, jumlah_kolom)

        # Menampilkan Gambar Papan Queens 
        papan_to_image(papan_final, papan_warna)

        print(f"Durasi pencarian : {durasi*100:.2f} ms")
        print(f"Banyak kasus yang ditinjau : {kasus} kasus\n")

        # Menyimpan Hasil Solusi
        print("==========================================================\n")
        opsi_simpan = input("Apakah Anda ingin menyimpan solusi? (Ya/Tidak) : ")
        while opsi_simpan != "Ya" and opsi_simpan != "Tidak":
            print(Fore.YELLOW + "Pilihan tidak valid, ulangi masukkan Anda!")
            opsi_simpan = input("Apakah Anda ingin menyimpan solusi? (Ya/Tidak) : ")

        if opsi_simpan == "Ya":
            save_file(papan_final, kasus, durasi, jumlah_queen)
        else:
            print("Papan tidak disimpan")


closing_statement()
