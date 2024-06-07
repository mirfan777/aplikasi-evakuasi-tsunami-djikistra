import heapq
from haversine import haversine, Unit
import folium
import webbrowser

def dijkstra_teraman(grafik, awal, node_tsunami, radius_tsunami, koordinat_tsunami):
    jarak = {node: float('inf') for node in grafik}
    jarak[awal] = 0
    predecessor = {node: None for node in grafik}
    antrean_prioritas = [(0, awal)]
    koordinat_node = {
        'A': (-7.320263597422809, 106.38700097895915),
        'B': (-7.327335645548595, 106.39379789658742),
        'C': (-7.346744809747519, 106.40006353675817),
        'D': (-7.31648366862809, 106.39994904743742),
        'E': (-7.3250310512411385, 106.42184570989399),
        'F': (-7.334834963647136, 106.44385137785989),
        'G': (-7.369222739821226, 106.40176628645538),
        'H': (-7.356241897165464, 106.43202231783063),
        'I': (-7.361327279085154, 106.45268502787167),
        'J': (-7.341388139768801, 106.42616224160027)
    }

    # Tambahkan koordinat untuk node tsunami
    koordinat_node[node_tsunami] = koordinat_tsunami

    node_dalam_radius = temukan_node_dalam_radius(koordinat_node, koordinat_tsunami, radius_tsunami)

    while antrean_prioritas:
        jarak_saat_ini, node_saat_ini = heapq.heappop(antrean_prioritas)

        if jarak_saat_ini > jarak[node_saat_ini]:
            continue

        for tetangga, bobot in grafik[node_saat_ini].items():
            jarak_ke_tetangga = jarak_saat_ini + bobot
            # pinalty jika node tetangga berada dalam radius tsunami
            if tetangga in node_dalam_radius:
                penalty = 1 / jarak_euclidean(koordinat_node[tetangga], koordinat_tsunami)
                jarak_ke_tetangga += penalty
                print( tetangga , jarak_ke_tetangga , jarak_euclidean(koordinat_node[tetangga], koordinat_tsunami))

            if jarak_ke_tetangga < jarak[tetangga]:  # Pindahkan baris ini ke bawah
                jarak[tetangga] = jarak_ke_tetangga
                if predecessor[node_saat_ini] is not None:
                    predecessor[tetangga] = node_saat_ini
                else:
                    predecessor[tetangga] = awal
                heapq.heappush(antrean_prioritas, (jarak_ke_tetangga, tetangga))

    return jarak, predecessor, koordinat_node

def jarak_euclidean(titik1, titik2):
    x1, y1 = titik1
    x2, y2 = titik2
    return haversine(titik1, titik2, unit=Unit.METERS)

def temukan_node_dalam_radius(koordinat_node, koordinat_tsunami, radius_tsunami):
    node_dalam_radius = []
    for node, koordinat in koordinat_node.items():
        jarak_ke_tsunami = jarak_euclidean(koordinat, koordinat_tsunami)
        if jarak_ke_tsunami <= radius_tsunami:
            node_dalam_radius.append(node)
    return node_dalam_radius

def lacak_jalur(predecessor, awal, akhir):
    jalur = []
    node = akhir
    while node != awal:
        jalur.append(node)
        if node not in predecessor or predecessor[node] is None:
            break
        node = predecessor[node]
    jalur.append(awal)
    jalur.reverse()
    return jalur

# Definisikan grafik sebagai dictionary dari dictionary
grafik = {
    'A': {'B': 1000, 'D': 3000},
    'B': {'A': 1000, 'C': 2000, 'D': 1000},
    'C': {'B': 2000, 'E': 6000, 'G': 2000},
    'D': {'A': 3000, 'B': 1000, 'E': 3000},
    'E': {'D': 3000, 'F': 3000, 'J': 5000},
    'F': {'E': 3000, 'I': 6000, 'J': 3000},
    'G': {'C': 2000, 'H': 5000, 'J': 8000},
    'H': {'G': 5000, 'I': 3000, 'J': 4000},
    'I': {'H': 3000, 'F': 6000},
    'J': {'G': 8000, 'H': 4000, 'E': 5000, 'F': 3000}
}

titik_tsunami = {
    'K': (-7.342662497731154, 106.37145236233276),
    'L': (-7.394529726795235, 106.44319618091892),
    'M': (-7.385166771948171, 106.39358604396786)
}

for key in titik_tsunami:
    print('Titik Posisi Tsunami', key, 'dengan titik koordinat', titik_tsunami[key])

# INPUT
koordinat_tsunami = input("Masukkan Posisi Tsunami (K/L/M): ")  # Koordinat node tsunami
if koordinat_tsunami.upper() in titik_tsunami:
    node_tsunami = koordinat_tsunami.upper()
    koordinat_tsunami = titik_tsunami[node_tsunami]
else:
    print('Tidak ada titik posisi tsunami', koordinat_tsunami)
    exit()  # Keluar dari program jika input tidak valid

node_awal = input("Masukkan node awal: ")  # Node awal
node_awal = node_awal.upper()
radius_tsunami = int(input("Masukkan radius tsunami (meter): "))  # Radius tsunami

jarak, predecessor, koordinat_node = dijkstra_teraman(grafik, node_awal, node_tsunami, radius_tsunami, koordinat_tsunami)

# Temukan node paling aman menggunakan perhitungan jarak dari koordinat ke pusat tsunami
node_teraman_tercepat = None
min_jarak_ke_tsunami = float('inf')
jarak_node_awal_ke_tsunami = jarak_euclidean(koordinat_node[node_awal], koordinat_tsunami)

for node, koordinat in koordinat_node.items():
    if node!= node_awal:
        jarak_ke_tsunami = jarak_euclidean(koordinat, koordinat_tsunami)
        if jarak_ke_tsunami > radius_tsunami and jarak[node] < float('inf'):
            if jarak[node] < min_jarak_ke_tsunami:
                min_jarak_ke_tsunami = jarak[node]
                node_teraman_tercepat = node

# Jika node awal sudah merupakan node terjauh dari tsunami, tidak ada node tujuan
if node_teraman_tercepat is None:
    # Jika node awal sudah merupakan node terjauh dari tsunami, tidak ada node tujuan
    if jarak_node_awal_ke_tsunami > min_jarak_ke_tsunami: # type: ignore
        print(f"Node {node_awal} sudah merupakan node terjauh dari pusat tsunami.")
        jalur_terpendek = [node_awal]
    else:
        print(f"Tidak ada posisi yang aman dari node {node_awal} dengan radius tsunami {radius_tsunami} pada koordinat {koordinat_tsunami}")
        jalur_terpendek=[]
else:
    jalur_terpendek = lacak_jalur(predecessor, node_awal, node_teraman_tercepat)
    print(f"Posisi teraman dan terdekat dari node {node_awal} adalah node {node_teraman_tercepat}")
    print(f"Node yang harus dilalui dari {node_awal} ke {node_teraman_tercepat} adalah: {jalur_terpendek}")

# Buat peta Sukabumi
peta = folium.Map(location=[-7.342662497731154, 106.37145236233276], zoom_start=12)

# Tambahkan node ke peta
for node, koordinat in koordinat_node.items():
    if node == node_awal:
        folium.Marker(koordinat, tooltip=node, icon=folium.Icon(color='red')).add_to(peta)
    elif node == node_teraman_tercepat:
        folium.Marker(koordinat, tooltip=node, icon=folium.Icon(color='blue')).add_to(peta)
    elif node in jalur_terpendek:
        folium.Marker(koordinat, tooltip=node, icon=folium.Icon(color='green')).add_to(peta)
    else:
        folium.Marker(koordinat, tooltip=node, icon=folium.Icon(color='black')).add_to(peta)
        

# Tambahkan edge ke peta
for node1, tetangga in grafik.items():
    for node2, bobot in tetangga.items():
        koordinat1 = koordinat_node[node1]
        koordinat2 = koordinat_node[node2]
        color = 'gray'
        if node1 in jalur_terpendek and node2 in jalur_terpendek:
            if abs(jalur_terpendek.index(node1) - jalur_terpendek.index(node2)) == 1:
                color = 'green'
        folium.PolyLine([koordinat1, koordinat2], tooltip=f"{node1} - {node2} (Bobot: {bobot})", color=color).add_to(peta)

# Tambahkan lingkaran untuk radius tsunami
folium.Circle(koordinat_tsunami, radius=radius_tsunami , color='red', fill=False).add_to(peta)

# Tambahkan layer control
folium.LayerControl().add_to(peta)

# Simpan peta ke file HTML
peta.save('peta.html')

# Buka peta di web browser
webbrowser.open('peta.html')

node_dalam_radius = temukan_node_dalam_radius(koordinat_node, koordinat_tsunami, radius_tsunami)
print(f"Node yang terkena radius tsunami {radius_tsunami} meter pada koordinat {koordinat_tsunami} adalah: {node_dalam_radius}")
