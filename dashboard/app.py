import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# memilih style
sns.set(style="darkgrid")

# memuat gambar logo
img = Image.open('bikerental1.png')

# menampilkan gambar di sidebar
st.sidebar.image(img)

# function untuk memuat data
@st.cache_data
def load_day_data():
    return pd.read_csv('data\day.csv')

@st.cache_data
def load_hour_data():
    return pd.read_csv('data\hour.csv')

@st.cache_data
def load_all_data():
    return pd.read_csv('all_data.csv')

# Memuat data semua data yg diperlukan
day_df = load_day_data()
hour_df = load_hour_data()
all_df = load_all_data()

# merubah type data dteday menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# function untuk memfilter data berdasarkan rentang waktu
def filter_data_by_date(df, start_date, end_date):
    filtered_df = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]
    return filtered_df

# sidebar untuk rentang waktu
st.sidebar.header("Rentang Waktu")
start_date = st.sidebar.date_input("Tanggal Awal", day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", day_df['dteday'].max())

# mengonversi start_date dan end_date ke format datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# memfilter data day dan all berdasarkan rentang waktu
filtered_day_df = filter_data_by_date(day_df, start_date, end_date)
filtered_all_df = filter_data_by_date(all_df, start_date, end_date)

# judul aplikasi
st.title(":bike: Bike Sharing Dashboard :bike:")

# visualisasi untuk pertanyaan 1
st.header("Pengguna Casual vs Registered")

plt.figure(figsize=(12, 8))
plt.plot(filtered_day_df['dteday'], filtered_day_df['casual'], label='Pengguna Casual', color='blue')
plt.plot(filtered_day_df['dteday'], filtered_day_df['registered'], label='Pengguna Registered', color='red')
plt.title('Pengguna Casual vs Pengguna Registered', fontsize=16)
plt.xlabel('Tanggal', fontsize=12)
plt.ylabel('Jumlah Pengguna', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)

# visualisasi data per jam dari hour.csv
st.header("Penyewaan Sepeda Per Jam")

# fungsi untuk mengelompokkan data per jam dari hour_df
hour_grouped = hour_df.groupby('hr').agg({'cnt': 'mean'}).reset_index()

# visualisasi untuk pertanyaan 2
plt.figure(figsize=(12, 8))
sns.lineplot(x='hr', y='cnt', data=hour_grouped)
plt.title('Rata-rata Penyewaan Sepeda Per Jam', fontsize=16)
plt.xlabel('Jam (0 - 23)', fontsize=12)
plt.ylabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=12)
plt.grid(True)
st.pyplot(plt)

# visualisasi data gabungan
st.header("Perbandingan Pengguna Casual, Registered, dan Total Penyewaan Sepeda per Jam")

plt.figure(figsize=(12, 8))
sns.lineplot(x='hr', y='casual', data=filtered_all_df, label='Casual', color='blue', marker='o')
sns.lineplot(x='hr', y='registered', data=filtered_all_df, label='Registered', color='red', marker='o')
sns.lineplot(x='hr', y='cnt', data=filtered_all_df, label='Total Penyewaan', color='green', marker='o')
plt.title('Perbandingan Pengguna Casual, Registered, dan Total Penyewaan Sepeda per Jam', fontsize=16)
plt.xlabel('Jam dalam Sehari (0-23)', fontsize=14)
plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
plt.grid(True)
plt.xticks(range(0, 24))
plt.legend(title='Tipe Pengguna', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# menampilkan ringkasan penyewaan sepeda
st.subheader("Ringkasan Penyewaan Sepeda")
col1, col2, col3 = st.columns(3)

# total penyewaan
total_rentals = filtered_day_df['cnt'].sum()
col1.metric("Total Penyewaan Sepeda", total_rentals)

# pengguna Casual
total_casual = filtered_day_df['casual'].sum()
col2.metric("Total Pengguna Casual", total_casual)

# pengguna Registered
total_registered = filtered_day_df['registered'].sum()
col3.metric("Total Pengguna Registered", total_registered)  

# footer
st.write("Bike Sharing © 2024")
