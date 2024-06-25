import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly_express as px


st.set_page_config(
    page_title="Understanding Kmeans Principles in Clustering Algorithms",
    page_icon="📊",
    layout="wide",  # Set layout to wide for full-width content
    initial_sidebar_state="collapsed",  # Collapse the sidebar by default
) 

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

 
st.header(" UNDERSTANDING ALGORITMA KMEANS ")
st.markdown(
 """
 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
 <hr>

<div class="card mb-3">
<div class="card">
  <div class="card-body">
    <h3 class="card-title" style="color:#007710;"><strong>⏱ PEMAHAMAN ALGORITMA KMEANS DALAM KLASTERISASI POPULASI</strong></h3>
    <p class="card-text">Algoritma KMeans mengelompokkan data dengan mencoba memisahkan sampel ke dalam n kelompok dengan varian yang sama, meminimalkan kriteria yang dikenal sebagai inersia atau jumlah kuadrat dalam cluster. Algoritma ini memerlukan jumlah cluster yang harus ditentukan. Ini berskala baik untuk sejumlah besar sampel dan telah digunakan di berbagai bidang aplikasi di berbagai bidang.</p>
    <p class="card-text">Algoritme K-means membagi satu set sampel ke dalam cluster yang terpisah-pisah, masing-masing dijelaskan dengan mean sampel yang ada di cluster tersebut. Sarana tersebut umumnya disebut cluster “centroids”; perhatikan bahwa secara umum poin-poin tersebut bukan berasal dari, meskipun mereka tinggal di ruang yang sama.</p>
    <p class="card-text">Algoritma KMeans bekerja dengan mencoba meminimalkan inersia atau jumlah kuadrat dalam cluster. Inersia diukur sebagai jumlah jarak kuadrat antara setiap sampel dalam cluster dengan centroidnya. Proses ini melibatkan iterasi di mana setiap sampel ditempatkan dalam cluster berdasarkan jarak Euclidean ke centroid terdekat. Centroid diupdate dengan menghitung mean dari semua sampel dalam cluster, dan proses ini diulangi hingga konvergensi.</p>
    <p class="card-text">Algoritma ini memerlukan jumlah cluster sebagai parameter input, dan pemilihan jumlah cluster yang tepat dapat dilakukan dengan menggunakan metode seperti Elbow Method.</p>
  </div>
</div>
</div>
 <style>
    [data-testid=stSidebar] {
         color: white;
         text-size:24px;
    }
</style>
""",unsafe_allow_html=True
)

with st.expander("⬇ RUMUS SSE (Sum of Squared Errors) :"):
     st.latex(r"SSE = \sum_{i=1}^{k} \sum_{j=1}^{n} ||x_{ij} - c_i||^2")
     st.write("di mana:")
     st.write("𝑘 adalah jumlah klaster yang diuji,")
     st.write("𝑛 adalah jumlah total sampel data,")
     st.write("𝑥𝑖𝑗 adalah sampel data ke-𝑗 dalam klaster ke-𝑖,,")
     st.write("𝑐𝑖 adalah centroid dari klaster ke-𝑖,")
     st.write("∣∣𝑥𝑖𝑗−𝑐𝑖∣∣2 adalah jarak kuadrat antara sampel data 𝑥𝑖𝑗 dan centroid klaster 𝑐𝑖.")

df=pd.read_csv("Data_Original_Update.csv")
#logo

# Pilih fitur yang ingin digunakan untuk klasterisasi
features_kmeans = df[['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']]

# Sample DataFrame
df_sample = df.sample(n=10)  # Ambil sampel 10 desa

# Ekspander untuk menampilkan data
with st.expander("⬇ DATA UNDERSTANDING FOR KMEANS :"):
    # Display summary statistics
    st.write("### Summary Statistics:")
    st.write(df.describe())
    st.write("Pendekatan statistik dari data populasi memberikan wawasan mendalam tentang karakteristik keseluruhan dari dataset. Dengan menganalisis statistik deskriptif, seperti yang ditampilkan di atas, kita dapat melihat gambaran umum tentang bagaimana nilai-nilai tersebar, tendensi sentral, dan sebaran data.")

    st.write("Selain itu, pendekatan inferensial dapat digunakan untuk membuat estimasi atau pengambilan keputusan lebih lanjut berdasarkan sampel data yang diambil dari populasi. Misalnya, penggunaan interval kepercayaan atau pengujian hipotesis dapat memberikan pemahaman lebih lanjut tentang parameter populasi.")

    st.write("Analisis spasial dengan mempertimbangkan koordinat geografis (Latitude dan Longitude), seperti yang terdapat dalam dataset, juga dapat membantu mengidentifikasi pola atau keterkaitan spasial di antara entitas populasi, memberikan wawasan lebih lanjut dalam konteks geografis.")

    

# Choose the column for the line chart
selected_column = '2023'

# Calculate quartiles
quartiles = df[selected_column].quantile([0.25, 0.5, 0.75])

# Create columns for expanders
c1, c2, c3 = st.columns(3)

with c1:
    with st.expander("⬇ QUARTILE TIDAK PADAT"):
        # Display quartile values
        st.write(f"**Quartile Information for {selected_column}:**")
        st.write(f"- 0.25% Percentile (Q1): {quartiles[0.25]}")

        # Line chart for the 25th percentile
        fig = px.line(df, x=df.index, y=selected_column, title="Line Chart - 25th Percentile (Q1)")
        fig.update_layout(height=300, width=400)  # Adjust the size
        st.plotly_chart(fig)

with c2:
    with st.expander("⬇ QUARTILE PADAT"):
        # Display quartile values
        st.write(f"**Quartile Information for {selected_column}:**")
        st.write(f"- 50th Percentile (Q2): {quartiles[0.5]}")

        # Line chart for the 50th percentile
        fig = px.line(df, x=df.index, y=selected_column, title="Line Chart - 50th Percentile (Q2)")
        fig.update_layout(height=300, width=400)  # Adjust the size
        st.plotly_chart(fig)

with c3:
    with st.expander("⬇ QUARTILE SANGAT PADAT"):
        # Display quartile values
        st.write(f"**Quartile Information for {selected_column}:**")
        st.write(f"- 75th Percentile (Q3): {quartiles[0.75]}")

        # Line chart for the 75th percentile
        fig = px.line(df, x=df.index, y=selected_column, title="Line Chart - 75th Percentile (Q3)")
        fig.update_layout(height=300, width=400)  # Adjust the size
        st.plotly_chart(fig)

# Membuat ekspander untuk menampilkan korelasi
with st.expander("⬇ EKSPLORASI VARIABEL:"):
    st.subheader("Korelasi antara Variabel")
    st.write("Melihat matriks korelasi antara variabel dalam dataset.")
    
    # Ganti df_selection dengan dataframe yang ingin Anda gunakan
    selected_features = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    
    # Hitung matriks korelasi
    correlation_matrix = df[selected_features].corr()

    # Plot heatmap using Plotly Express
    fig = px.imshow(correlation_matrix,
                    labels=dict(x="Features", y="Features", color="Correlation"),
                    x=selected_features,
                    y=selected_features,
                    color_continuous_scale="viridis",  # Use 'viridis' instead of 'coolwarm'
                    title="Heatmap Korelasi")

    
    # Show the plot
    st.plotly_chart(fig)
    

    st.write("Visualisasi ini memberikan gambaran distribusi univariat dari setiap variabel dalam dataset. Histogram menunjukkan sebaran nilai-nilai di setiap variabel, dan kernel density estimation (KDE) memberikan perkiraan kurva distribusi.")

# checking null value
with st.expander("⬇ NULL VALUES, TENDENCY & VARIABLE DISPERSION"):
    a1, a2 = st.columns(2)
    a1.write("Jumlah nilai yang hilang (NaN atau None) di setiap kolom dalam DataFrame")
    a1.dataframe(df.isnull().sum(), use_container_width=True)

    a2.write("Insight ke dalam kecenderungan sentral, dispersi, dan distribusi data.")
    a2.dataframe(df.describe().T, use_container_width=True)

X = df[['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']]
kmeans = KMeans(n_clusters=2, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

# Metode Elbow untuk menentukan jumlah klaster optimal
distortions = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(features_kmeans)
    distortions.append(kmeans.inertia_)

# Menghitung Silhouette Score untuk berbagai jumlah klaster
silhouette_scores = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    labels = kmeans.fit_predict(features_kmeans)
    silhouette_scores.append(silhouette_score(features_kmeans, labels))

c1, c2, c3 = st.columns(3)

with c1:
    with st.expander("⬇ ELBOW METHOD"):
        st.write("Metode Elbow digunakan untuk menentukan jumlah klaster optimal dalam algoritma KMeans.")
        
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(range(1, 11), distortions, marker='o')
        ax.set_title('Metode Elbow untuk Menentukan Jumlah Klaster Optimal')
        ax.set_xlabel('Jumlah Klaster')
        ax.set_ylabel('Distorsi')
        
        # Pass the figure to st.pyplot
        st.pyplot(fig)

# Visualisasi Silhouette Score
with c2:
    with st.expander("⬇ SILHOUETTE SCORE"):
        st.write("Silhouette Score digunakan untuk mengukur sejauh mana klaster terpisah dan saling berdekatan.")

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(range(2, 11), silhouette_scores, marker='o')
        ax.set_title('Silhouette Score untuk Menentukan Jumlah Klaster Optimal')
        ax.set_xlabel('Jumlah Klaster')
        ax.set_ylabel('Silhouette Score')
        
        # Pass the figure to st.pyplot
        st.pyplot(fig)

# Kesimpulan
with c3:
    with st.expander("⬇ KESIMPULAN"):
        st.write("Berdasarkan analisis menggunakan Elbow Method dan Silhouette Score, kita dapat menyimpulkan:")
        
        # Menentukan jumlah klaster optimal dari Elbow Method
        optimal_clusters = 2  # Ganti dengan hasil analisis Elbow Method
        st.write(f"Jumlah klaster optimal berdasarkan Elbow Method: {optimal_clusters}")
        
        # Menampilkan Silhouette Score tertinggi
        best_silhouette_score = max(silhouette_scores)
        st.write(f"Silhouette Score tertinggi: {best_silhouette_score}")



# Display the scatter plot using Plotly Express
with st.expander("⬇ CLUSTER VISUALIZATION"):
    
    fig = px.scatter(df, x='2022', y='2023', color='Cluster',
                 title="Clusters", labels={'2022': '2022', '2023': '2023'},
                 color_continuous_scale='viridis', size_max=10)
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)
