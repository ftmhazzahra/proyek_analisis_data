import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read CSV files
day_df = pd.read_csv("data/day.csv", index_col="instant", parse_dates=["dteday"])
hour_df = pd.read_csv("data/hour.csv", index_col="instant", parse_dates=["dteday"])

# Dashboard Title
st.title('Dashboard Analisis Data Sepeda')

# Sidebar
st.sidebar.subheader('Pilih Analisis Data')
analysis_choice = st.sidebar.radio("Pilih Analisis:", ('Tren Jumlah Sepeda per Jam', 'Rata-rata Sepeda Disewakan per Musim',
                                                       'Rata-rata Sepeda Disewakan per Bulan', 'Rata-rata Sepeda Disewakan per Hari dalam Seminggu',
                                                       'Rata-rata Sepeda Disewakan per Hari Libur vs. Hari Kerja', 'Jumlah Penyewa per Tanggal'))

# Data Analysis
if analysis_choice == 'Tren Jumlah Sepeda per Jam':
    st.subheader('Tren Jumlah Sepeda per Jam')
    st.write("Ini adalah grafik yang menunjukkan tren jumlah sepeda disewakan per jam.")
    st.write("Grafik ini membagi data berdasarkan musim dan menggambarkan perubahan jumlah sepeda disewakan sepanjang hari.")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hour_df, x='hr', y='cnt', hue='season', palette='husl', linewidth=2.5, ax=ax)
    ax.set_title('Tren Jumlah Sepeda Disewakan per Jam')
    ax.set_xlabel('Jam (hr)')
    ax.set_ylabel('Jumlah Sepeda Disewakan')
    ax.legend(title='Musim', loc='upper right', labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

elif analysis_choice == 'Rata-rata Sepeda Disewakan per Musim':
    st.subheader('Rata-rata Sepeda Disewakan per Musim')
    st.write("Ini adalah grafik yang menampilkan rata-rata jumlah sepeda disewakan untuk setiap musim.")
    data_per_musim = day_df.groupby('season')['cnt'].mean()
    nama_musim = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(nama_musim.values(), data_per_musim.values)
    ax.set_title('Rata-rata Jumlah Sepeda Disewakan Per Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Sepeda Disewakan')
    ax.set_xticklabels(nama_musim.values(), rotation=15, ha='right')
    st.pyplot(fig)

elif analysis_choice == 'Rata-rata Sepeda Disewakan per Bulan':
    st.subheader('Rata-rata Sepeda Disewakan per Bulan')
    st.write("Ini adalah grafik yang menunjukkan rata-rata jumlah sepeda disewakan per bulan.")
    data_per_bulan = day_df.groupby('mnth')['cnt'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data_per_bulan.index, data_per_bulan.values, marker='o', linestyle='-')
    ax.set_title('Jumlah Sepeda Disewakan Per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Sepeda Disewakan')
    ax.grid(True)
    ax.set_xticks(data_per_bulan.index)
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
    st.pyplot(fig)

elif analysis_choice == 'Rata-rata Sepeda Disewakan per Hari dalam Seminggu':
    st.subheader('Rata-rata Sepeda Disewakan per Hari dalam Seminggu')
    st.write("Ini adalah grafik yang menampilkan rata-rata jumlah sepeda disewakan per hari dalam seminggu.")
    data_per_hari = day_df.groupby('weekday')['cnt'].mean()
    nama_hari = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(nama_hari, data_per_hari.values)
    ax.set_title('Rata-rata Jumlah Sepeda Disewakan per Hari dalam Seminggu')
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Rata-rata Jumlah Sepeda Disewakan')
    ax.set_xticklabels(nama_hari, rotation=45)
    st.pyplot(fig)

elif analysis_choice == 'Rata-rata Sepeda Disewakan per Hari Libur vs. Hari Kerja':
    st.subheader('Rata-rata Sepeda Disewakan per Hari Libur vs. Hari Kerja')
    st.write("Ini adalah grafik yang menampilkan rata-rata jumlah sepeda disewakan per hari libur dan hari kerja.")
    data_hari_libur = day_df[day_df['holiday'] == 1]['cnt'].mean()
    data_hari_kerja = day_df[day_df['workingday'] == 1]['cnt'].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Hari Libur', 'Hari Kerja'], [data_hari_libur, data_hari_kerja])
    ax.set_title('Rata-rata Jumlah Sepeda Disewakan per Hari Libur vs. Hari Kerja')
    ax.set_xlabel('Jenis Hari')
    ax.set_ylabel('Rata-rata Jumlah Sepeda Disewakan')
    st.pyplot(fig)

elif analysis_choice == 'Jumlah Penyewa per Tanggal':
    st.subheader('Jumlah Penyewa per Tanggal')
    selected_date = st.date_input("Pilih Tanggal", value=pd.to_datetime('2011-01-01'))
    
    # Filter data for the selected date
    selected_date_data = day_df[day_df['dteday'].dt.date == selected_date]
    
    if not selected_date_data.empty:
        rental_count = selected_date_data['cnt'].sum()
        st.write(f"Jumlah penyewa pada {selected_date} adalah {rental_count}.")
    else:
        st.write(f"Tidak ada data penyewaan untuk tanggal {selected_date}.")

# Conclusion
st.sidebar.subheader('Kesimpulan dan Implikasi')
st.sidebar.write("**Conclusion Pertanyaan 1:** Bagaimana tren penyewaan sepeda berubah sepanjang tahun dan apa faktor-faktor yang paling memengaruhinya?")
st.sidebar.write("Dari analisis data yang telah dilakukan, kami dapat mengambil kesimpulan sebagai berikut:")
st.sidebar.write("Tren penyewaan sepeda memiliki pola musiman yang jelas, dengan peningkatan penyewaan selama musim panas dan gugur. Faktor-faktor seperti musim, suhu, serta kondisi cuaca berpengaruh besar terhadap tren penyewaan sepeda. Penyewaan sepeda biasanya lebih tinggi pada hari kerja dibandingkan dengan akhir pekan atau hari libur.")

st.sidebar.write("**Conclusion Pertanyaan 2:** Bagaimana pola musiman dalam penyewaan sepeda dapat membantu dalam pengambilan keputusan persediaan sepeda yang lebih efektif?")
st.sidebar.write("Pola Musiman dalam Penyewaan Sepeda:")
st.sidebar.write("- Musim Panas (Summer): Rata-rata Jumlah Sepeda Disewakan = 4992.33")
st.sidebar.write("- Musim Gugur (Fall): Rata-rata Jumlah Sepeda Disewakan = 5644.3")

st.sidebar.write("Pola Harian dalam Penyewaan Sepeda:")
st.sidebar.write("- Hari Kerja (Weekday): Rata-rata Jumlah Sepeda Disewakan = 4584.82")
st.sidebar.write("- Hari Libur (Weekend): Rata-rata Jumlah Sepeda Disewakan = 3735.0")

st.sidebar.write("**Implikasi:**")
st.sidebar.write("Selama musim panas dan gugur, permintaan penyewaan sepeda meningkat tajam. Oleh karena itu, perlu ada peningkatan strategi persediaan untuk mengakomodasi lonjakan permintaan selama periode ini. Pada hari kerja, penyewaan sepeda lebih tinggi dibandingkan hari libur, menunjukkan adanya peluang bisnis di hari-hari kerja. Perusahaan dapat memanfaatkan ini dengan menerapkan strategi pemasaran dan promosi yang menarik untuk meningkatkan jumlah penyewa pada hari kerja. Analisis pola musiman ini memberikan wawasan penting untuk perencanaan persediaan, memungkinkan perusahaan mengoptimalkan manajemen inventaris untuk mencegah ketidakseimbangan antara persediaan dan permintaan. Dengan demikian, kepuasan pelanggan dapat meningkat, dan efisiensi operasional pun dapat diperbaiki.")
