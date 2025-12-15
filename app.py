# File: app.py (Virtual Lab Fibonacci Search - Single File Version)

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

# List global untuk menyimpan riwayat langkah
HISTORY = []

# =================================================================
# --- FUNGSI ALGORITMA FIBONACCI SEARCH (DIGABUNGKAN KE SINI) ---
# =================================================================

def fibonacci_search(data_list, target):
    """
    Mengimplementasikan Fibonacci Search dan mencatat setiap langkah di HISTORY.
    """
    global HISTORY
    HISTORY = []
    
    # Prasyarat: Array harus terurut!
    arr = sorted(data_list[:]) 
    n = len(arr)
    
    if n == 0:
        HISTORY.append({'array': arr[:], 'target': target, 'status': 'Selesai', 'action': 'Array kosong.'})
        return -1, HISTORY

    # 1. Menentukan Bilangan Fibonacci
    # Cari bilangan Fibonacci F(k) terkecil yang lebih besar atau sama dengan n
    fib_m2 = 0  # F(k-2)
    fib_m1 = 1  # F(k-1)
    fib_k = fib_m1 + fib_m2  # F(k)
    
    while fib_k < n:
        fib_m2 = fib_m1
        fib_m1 = fib_k
        fib_k = fib_m1 + fib_m2
    
    # offset digunakan untuk melacak rentang yang dibuang
    offset = -1 
    
    HISTORY.append({
        'array': arr[:], 'target': target, 'offset': offset, 'fib_k': fib_k,
        'fib_m1': fib_m1, 'fib_m2': fib_m2, 'status': 'Mulai',
        'action': f'Memulai Fibonacci Search. Ukuran Array={n}. Fibonacci F(k)={fib_k}.'
    })

    # 2. Proses Pencarian
    while fib_k > 1:
        # Tentukan indeks yang akan diperiksa (i)
        i = min(offset + fib_m2, n - 1)
        
        # Catat langkah pengecekan
        HISTORY.append({
            'array': arr[:], 'target': target, 'offset': offset, 'fib_k': fib_k,
            'fib_m1': fib_m1, 'fib_m2': fib_m2, 'check_index': i,
            'status': 'Mengecek',
            'action': f'Mengecek Indeks {i} (Nilai: {arr[i]}). Dibagi berdasarkan F(k-2)={fib_m2}.'
        })

        if arr[i] < target:
            # Target ada di blok KANAN (ukuran F(k-1)). Buang F(k-2) dan offset.
            fib_k = fib_m1        # F(k) menjadi F(k-1)
            fib_m1 = fib_m2       # F(k-1) menjadi F(k-2)
            fib_m2 = fib_k - fib_m1 # F(k-2) menjadi F(k) - F(k-1)
            offset = i            # Pindahkan batas offset ke indeks yang baru
            
            HISTORY.append({
                'array': arr[:], 'target': target, 'offset': offset, 'fib_k': fib_k,
                'fib_m1': fib_m1, 'fib_m2': fib_m2, 'check_index': i,
                'status': 'Pindah Kanan',
                'action': f'Nilai terlalu kecil. Pindah ke blok kanan. Offset baru: {offset}.'
            })

        elif arr[i] > target:
            # Target ada di blok KIRI (ukuran F(k-2)). Buang F(k-1).
            fib_k = fib_m2        # F(k) menjadi F(k-2)
            fib_m1 = fib_m1 - fib_m2 # F(k-1) menjadi F(k-1) - F(k-2)
            fib_m2 = fib_k - fib_m1 # F(k-2)
            # offset tetap
            
            HISTORY.append({
                'array': arr[:], 'target': target, 'offset': offset, 'fib_k': fib_k,
                'fib_m1': fib_m1, 'fib_m2': fib_m2, 'check_index': i,
                'status': 'Pindah Kiri',
                'action': f'Nilai terlalu besar. Pindah ke blok kiri. Offset tetap.'
            })

        else:
            # Ditemukan
            HISTORY.append({
                'array': arr[:], 'target': target, 'offset': offset, 'fib_k': fib_k,
                'fib_m1': fib_m1, 'fib_m2': fib_m2, 'check_index': i,
                'status': 'Ditemukan',
                'action': f'Nilai {target} DITEMUKAN pada Indeks {i}!'
            })
            return i, HISTORY

    # 3. Pengecekan Akhir (Sisa satu elemen)
    if fib_m1 == 1 and arr[offset + 1] == target:
        i = offset + 1
        HISTORY.append({
            'array': arr[:], 'target': target, 'offset': offset, 'fib_k': 1,
            'fib_m1': 1, 'fib_m2': 0, 'check_index': i,
            'status': 'Ditemukan',
            'action': f'Pengecekan akhir. Nilai {target} DITEMUKAN pada Indeks {i}!'
        })
        return i, HISTORY

    # Tidak ditemukan
    HISTORY.append({
        'array': arr[:], 'target': target, 'offset': offset, 'fib_k': fib_k,
        'fib_m1': fib_m1, 'fib_m2': fib_m2, 'check_index': -1,
        'status': 'Selesai',
        'action': f'Pencarian selesai. Nilai {target} tidak ditemukan.'
    })
    return -1, HISTORY

# =================================================================
# --- KONFIGURASI DAN STREAMLIT APP ---
# =================================================================

st.set_page_config(
    page_title="Virtual Lab: Fibonacci Search",
    layout="wide"
)

st.title("🐇 Virtual Lab: Fibonacci Search Interaktif")
st.markdown("### Visualisasi Algoritma Pencarian Berbasis Deret Fibonacci")


st.sidebar.header("Konfigurasi Data dan Target")

# Contoh data yang terurut
default_data = "1, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610" 
input_data_str = st.sidebar.text_input(
    "Masukkan data terurut (pisahkan dengan koma):", 
    default_data
)
target_value_str = st.sidebar.text_input("Masukkan Nilai Target yang Dicari:", "55")
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    if not data_list:
        st.error("Masukkan setidaknya satu angka untuk array.")
        st.stop()
    target_value = int(target_value_str.strip())
    initial_data_sorted = sorted(list(data_list))
except ValueError:
    st.error("Pastikan semua input data dan target adalah angka (integer) yang dipisahkan oleh koma.")
    st.stop()

# --- Penjelasan Pewarnaan ---
st.markdown("""
#### Pewarnaan Bar:
* **Hijau:** Indeks **Pengecekan (i)** yang sedang dibandingkan.
* **Kuning:** Rentang **Pencarian Aktif** (Area yang dipecah oleh Bilangan Fibonacci).
* **Merah:** Bagian array yang sudah **dibuang** atau dilewati oleh `offset`.
* **Biru:** Indeks **Offset** (Batas bawah rentang pencarian Fibonacci).
* **Ungu:** Indeks di mana nilai **ditemukan**.
""")

st.write(f"**Array Terurut (Prasyarat):** {initial_data_sorted}")
st.write(f"**Nilai Target:** **{target_value}**")

# --- Fungsi Plot Matplotlib ---
def plot_array(arr, state, found_index, max_val):
    fig, ax = plt.subplots(figsize=(12, 4))
    n = len(arr)
    x_pos = np.arange(n)
    target = state['target']
    
    colors = ['#CC0000'] * n # Merah: Default / Dibuang
    status = state['status']
    
    offset = state.get('offset', -1)
    check_index = state.get('check_index', -1)
    
    # Menentukan rentang aktif (Kuning)
    # Rentang aktif adalah dari offset + 1 hingga N-1 (atau batas efektif array)
    start_active = offset + 1
    end_active = n 
    
    for k in range(start_active, end_active):
        colors[k] = '#F1C232' # Kuning: Rentang Aktif

    # Biru: Offset (Batas Bawah Fibonacci)
    if offset != -1 and offset < n:
         colors[offset] = '#4A86E8' 

    # Hijau: Indeks Pengecekan (i)
    if check_index != -1 and check_index < n and status != 'Ditemukan':
        colors[check_index] = '#6AA84F'

    # Ungu (#8E44AD): Ditemukan
    if found_index != -1:
        colors[found_index] = '#8E44AD'
        
    ax.bar(x_pos, arr, color=colors)
    
    # Menambahkan label offset dan check_index
    if offset != -1 and offset < n:
        ax.text(offset, max_val * 1.05, f'OFFSET ({offset})', color='darkblue', ha='center', fontsize=10, weight='bold')
    
    if check_index != -1 and check_index < n:
        if status != 'Ditemukan':
             ax.text(check_index, max_val * 0.95, f'CEK ({check_index})', color='darkgreen', ha='center', fontsize=10, weight='bold')
        
    # Menambahkan Label Angka di Atas Bar
    for k, height in enumerate(arr):
        ax.text(x_pos[k], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    ax.set_ylim(0, max_val * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'I: {k}' for k in range(n)], rotation=0) 
    ax.set_ylabel('Nilai')
    ax.set_title(f"Pencarian Nilai: {target}", fontsize=14)
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama ---
if st.button("Mulai Simulasi Fibonacci Search"):
    
    found_index, history = fibonacci_search(list(data_list), target_value)
    max_data_value = max(initial_data_sorted) if initial_data_sorted else 10 
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
        status_placeholder = st.empty() 
    with col2:
        table_placeholder = st.empty()
    
    final_found_index = -1
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        status = state['status']
        action = state['action']

        if status == 'Ditemukan':
            final_found_index = state.get('check_index')
        
        fig_mpl = plot_array(current_array, state, final_found_index, max_data_value)

        with vis_placeholder.container():
            st.pyplot(fig_mpl, clear_figure=True)
        
        with table_placeholder.container():
             df_table = pd.DataFrame({'Index': range(len(current_array)), 'Nilai': current_array})
             st.markdown("##### Data Array (Index & Nilai)")
             st.dataframe(df_table.T, hide_index=True)

        with status_placeholder.container():
            if status == 'Ditemukan':
                st.success(f"**Langkah ke-{step}** | **Status:** {status}")
            elif status == 'Selesai':
                st.error(f"**Langkah ke-{step}** | **Status:** {status}")
            else:
                 st.info(f"**Langkah ke-{step+1}** | **Status:** {status}")
            st.caption(action)

        time.sleep(speed)

    # --- Hasil Akhir Final ---
    st.markdown("---")
    if final_found_index != -1:
        st.balloons()
        st.success(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** DITEMUKAN pada Indeks **{final_found_index}**.")
    else:
        st.error(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** TIDAK DITEMUKAN dalam array.")
    
    st.info(f"Algoritma Fibonacci Search selesai dalam **{len(history)-1}** langkah visualisasi.")
