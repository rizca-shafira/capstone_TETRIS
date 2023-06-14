import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
#from numerize import numerize

st.set_page_config(
    page_title = 'Capstone TETRIS',
    layout = 'wide'
)

with st.container():
    st.title('Pola Konsumsi Sambal Indonesia')
    st.write('Oleh : 144 - Rizca Shafira Salsabila Makasuci | rizcashafira04@gmail.com')
    st.write('Sambal adalah bumbu populer berbasis cabai yang tak terpisahkan dari masakan Indonesia. Dalam proyek ini, fokus analisis adalah memahami pola konsumsi sambal di Indonesia melalui pemanfaatan data yang relevan untuk mengungkap preferensi dan kebiasaan konsumsi masyarakat terkait sambal.')

df = pd.read_csv('clean data bumbu.csv')

with st.expander("Rata-rata Pengeluaran Perkapita Seminggu Sambal Jadi Per Kabupaten/Kota (Rupiah/Kapita/Minggu) 2018 - 2022"):
    df.columns = ['Kabupaten/Kota', 'Konsumsi Sambal Jadi', 'Tahun', 'Provinsi']
    st.dataframe(df, use_container_width=True)
    # Rename the columns for better understanding
    st.write('Sumber : BPS (https://www.bps.go.id/indicator/5/2122/1/rata-rata-pengeluaran-perkapita-seminggu-menurut-kelompok-bumbu-bumbuan-per-kabupaten-kota.html)')

# Calculate total sambal consumption across all cities and provinces over the years
data = pd.pivot_table(
    data=df,
    index='Tahun',
    values='Konsumsi Sambal Jadi',
    aggfunc='mean'
).reset_index()

# Rename the columns for better understanding
data.columns = ['Tahun', 'Rata-rata Konsumsi']

# Print the analysis results
# st.dataframe(data)

# Determine the minimum and maximum years from DataFrame
min_year = data['Tahun'].min()
max_year = data['Tahun'].max()

# Make line chart for average consumption each year
consumption_avg_line = alt.Chart(data).mark_line().encode(
    alt.X('Tahun', title='Tahun', scale=alt.Scale(domain=[min_year, max_year])),
    alt.Y('Rata-rata Konsumsi', title='Rata-rata Konsumsi (Rupiah/Kapita/Minggu)')
).configure_axis(
    labelExpr="datum.value + ''" # Remove formatting with commas
)

# Calculate the average konsumsi sambal for each Kota and Provinsi
pivot_kota = df.pivot_table(values='Konsumsi Sambal Jadi', index='Kabupaten/Kota', aggfunc='mean')
pivot_provinsi = df.pivot_table(values='Konsumsi Sambal Jadi', index='Provinsi', aggfunc='mean')

# Create two columns
avg_chart, avg_text = st.columns(2)
with avg_chart:
    # Content for the first column
    st.write("Grafik Rata - Rata Konsumsi Sambal Jadi Per Kota/Kabupaten (Rupiah/Kapita/Minggu)")
    #Show line chart
    st.altair_chart(consumption_avg_line)

# Content for the second column
with avg_text:
    st.write("Tabel Peringkat Berdasarkan Konsumsi Sambal Jadi (Rupiah/Kapita/Minggu)")

    # Create two columns
    areacol, rankcol = st.columns(2)
    with areacol:
        area = st.selectbox("Area", ['Kabupaten/Kota','Provinsi'])

    with rankcol:
        rank = st.selectbox("Rank", ['Highest','Lowest'])
    
    # Perform nlargest or nsmallest based on the user's selection
    if rank == 'Highest':
        # Get the top 5 Kota and Provinsi based on average konsumsi sambal
        if area == 'Kabupaten/Kota':
            top_kota = pivot_kota.nlargest(5, 'Konsumsi Sambal Jadi')
            st.dataframe(top_kota, use_container_width=True)
        else:
            top_provinsi = pivot_provinsi.nlargest(5, 'Konsumsi Sambal Jadi')
            st.dataframe(top_provinsi, use_container_width=True)
    else:
        # Get the lowest 5 Kota and Provinsi based on average konsumsi sambal
        if area == 'Kabupaten/Kota':
            top_kota = pivot_kota.nsmallest(5, 'Konsumsi Sambal Jadi')
            st.dataframe(top_kota, use_container_width=True)
        else:
            top_provinsi = pivot_provinsi.nsmallest(5, 'Konsumsi Sambal Jadi')
            st.dataframe(top_provinsi, use_container_width=True)

dfbaru = pd.read_csv('clean data bumbu - reordered.csv')

with st.expander("Rata-rata Pengeluaran Perkapita Seminggu Sambal Jadi, Bumbu Racikan, dan Cabe Per Kabupaten/Kota (Rupiah/Kapita/Minggu) 2018 - 2022"):
    dfbaru.columns = ['Kabupaten/Kota', 'Provinsi', 'Sambal Jadi', 'Bumbu Racikan', 'Cabe Merah', 'Cabe Hijau', 'Cabe Rawit', 'Tahun']
    st.dataframe(dfbaru, use_container_width=True)
    # Rename the columns for better understanding
    st.write('Sumber : BPS (https://www.bps.go.id/indicator/5/2116/1/rata-rata-pengeluaran-perkapita-seminggu-menurut-kelompok-sayur-sayuran-per-kabupaten-kota.html)')

dfbaru_heatmap = dfbaru[['Sambal Jadi', 'Bumbu Racikan', 'Cabe Merah', 'Cabe Hijau', 'Cabe Rawit']].copy() 

# Calculate the correlation matrix
corr_matrix = dfbaru_heatmap.corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
# Set the title of the heatmap
ax.set_title('Correlation Heatmap')


# Create two columns
heatmap1, col2 = st.columns(2)
with heatmap1:
    # Content for the first column
    st.write("Heatmap Konsumsi Sambal Jadi, Bumbu Racikan, dan Cabe (Rupiah/Kapita/Minggu)")
    # Display the heatmap using Streamlit
    st.pyplot(fig)
