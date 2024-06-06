import streamlit as st
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import time
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, cophenet
from scipy.spatial.distance import pdist


# Set page configuration
st.set_page_config(
    page_title="AHC Algorithm Approach in Population Data Clustering",
    page_icon="📊",
    layout="wide",  # Set layout to wide for full-width content
    initial_sidebar_state="collapsed",  # Collapse the sidebar by default
)

# Function to perform Agglomerative Hierarchical Clustering
def ahc_clustering(data, n_clusters, linkage):
    features = data[['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']]
    
    # Fit AgglomerativeClustering
    clusterer = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    data['cluster'] = clusterer.fit_predict(features)
    
    # Calculate centroid for each cluster
    centroids = data.groupby('cluster')[['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']].mean()

        # Define threshold values (adjust these based on your analysis)
    threshold_low = 100000  # Example threshold for "not dense"
    threshold_high = 500000  # Example threshold for "dense"

    # Add Density Category column based on centroid values
    data['Density Category'] = data['cluster'].map(lambda cluster: 'Tidak Padat' if centroids.loc[cluster].mean() < threshold_low else ('Padat' if centroids.loc[cluster].mean() < threshold_high else 'Sangat Padat'))
    
    # After clustering, calculate silhouette score
    silhouette_avg = silhouette_score(features, data['cluster'])

    return data, silhouette_avg

# Function to calculate CCC for different linkage methods
def calculate_ccc(data):
    numeric_data = data.select_dtypes(include=['float64', 'int64']).copy()

    # Calculate CCC for 'single' linkage method
    linkage_matrix_single = linkage(numeric_data, method='single')
    cophenet_matrix_single, _ = cophenet(linkage_matrix_single, pdist(numeric_data))
    ccc_single = cophenet_matrix_single.mean()

    # Calculate CCC for 'average' linkage method
    linkage_matrix_average = linkage(numeric_data, method='average')
    cophenet_matrix_average, _ = cophenet(linkage_matrix_average, pdist(numeric_data))
    ccc_average = cophenet_matrix_average.mean()

    # Calculate CCC for 'complete' linkage method
    linkage_matrix_complete = linkage(numeric_data, method='complete')
    cophenet_matrix_complete, _ = cophenet(linkage_matrix_complete, pdist(numeric_data))
    ccc_complete = cophenet_matrix_complete.mean()

    return ccc_single, ccc_average, ccc_complete


# Function to display CCC Progress Bar
def CCCProgressBar(score, target, metode):
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)

    current = score
    percent = round((current / target * 100))
    mybar = st.progress(0)

    st.write(f"Metode yang dipilih: {metode}")

    if percent >= 100:
        st.subheader("Skor target tercapai!")
    else:
        st.write("Skor yang diCapai {:.2f}% dari skor target".format(percent))

        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1, text="Persentase Skor")
    

# Function to create GeoMap with Plotly Express
def create_geomap(data, geojson_data, selected_color_theme):
    # Merge GeoJSON data with clustered data based on 'DESA_1'
    merged_data = geojson_data.merge(data, left_on='DESA_1', right_on='DESA_1')

    # Sidebar to select 'DESA_1'
    selected_DESA = st.sidebar.selectbox("Pilih DESA_1", merged_data['DESA_1'].unique())

    # Filter data for selected 'DESA_1'
    filtered_df_DESA = merged_data[merged_data['DESA_1'] == selected_DESA]

    # Get coordinates for the selected 'DESA_1'
    selected_lon = filtered_df_DESA.geometry.centroid.x.values[0]
    selected_lat = filtered_df_DESA.geometry.centroid.y.values[0]

    # Plot GeoMap with Plotly Express
    fig = px.choropleth_mapbox(
        merged_data,
        geojson=merged_data.geometry,
        locations=merged_data.index,
        hover_name='DESA_1',
        color='cluster',
        color_continuous_scale=selected_color_theme,
        mapbox_style="carto-darkmatter",
        zoom=9.5,
        center={"lat": merged_data.geometry.centroid.y.mean(), "lon": merged_data.geometry.centroid.x.mean()},
        labels={'cluster': 'Cluster'}
    )

    # Add marker for the selected 'DESA_1'
    fig.add_trace(go.Scattermapbox(
        mode="markers+text",
        lon=[selected_lon],
        lat=[selected_lat],
        marker=dict(size=14, color="red"),
        text=[selected_DESA],
        hoverinfo='text',
        showlegend=False
    ))

    # Set the map layout
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    # Show the GeoMap
    st.plotly_chart(fig, use_container_width=True)


# Function to handle Agglomerative Hierarchical Clustering page
def ahc_page():
    center = True
    st.header("Agglomerative Hierarchical Clustering Page", anchor='center' if center else 'left')

    # Sidebar: Choose the number of clusters
    n_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=50, value=5)

    # Sidebar: Choose the linkage type
    linkage = st.sidebar.selectbox("Linkage Type", ['complete', 'single', 'average'])

    # Select Year in the Sidebar
    st.session_state.selected_year = st.sidebar.selectbox('Select Year', ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])

    # Load data from the home page
    data_from_homepage = pd.read_csv('AUDIT-Data_Original_Update.csv')  # Replace with your actual data

     # Perform Agglomerative Hierarchical Clustering
    df_clustered, silhouette_avg = ahc_clustering(data_from_homepage, n_clusters, linkage)

    # Calculate CCC for different linkage methods
    ccc_single, ccc_average, ccc_complete = calculate_ccc(data_from_homepage)

    # Save the clustered data and silhouette score in session_state
    st.session_state.df_clustered = df_clustered
    st.session_state.ccc_single = ccc_single
    st.session_state.ccc_average = ccc_average
    st.session_state.ccc_complete = ccc_complete

    

    tab1, tab2, tab3 = st.tabs(["DATASET", "VISUALISASI MAP", "SILLHOUTE SCORE FOR AHC METODE"])

    with tab1:
        
        # Menampilkan Progress Bar CCC berdasarkan jenis linkage yang dipilih
        if linkage == 'single':
            CCCProgressBar(st.session_state.ccc_single, target=1.0, metode='single')
        elif linkage == 'average':
            CCCProgressBar(st.session_state.ccc_average, target=1.0, metode='average')
        elif linkage == 'complete':
            CCCProgressBar(st.session_state.ccc_complete, target=1.0, metode='complete')

        # Menampilkan metrik untuk setiap klaster
        for cluster_num in range(n_clusters):
            # Get the density category for the current cluster
            density_category = df_clustered.loc[df_clustered['cluster'] == cluster_num, 'Density Category'].iloc[0]

            cluster_data = df_clustered[df_clustered['cluster'] == cluster_num][["DESA_1", "cluster", st.session_state.selected_year]]

            # Hitung jumlah anggota klaster
            num_members = cluster_data.shape[0]

            with st.expander(f"Cluster {cluster_num + 1} Data Table - {density_category} ({num_members} Anggota)", expanded=True):
                st.dataframe(cluster_data,
                            column_order=("DESA_1", st.session_state.selected_year, "cluster"),
                            hide_index=True,
                            width=500,
                            use_container_width=True,
                            column_config={
                                "DESA_1": st.column_config.TextColumn(
                                    "Area",
                                ),
                                st.session_state.selected_year: st.column_config.ProgressColumn(
                                    st.session_state.selected_year,
                                    format="%f",
                                    min_value=0,
                                    max_value=max(cluster_data[st.session_state.selected_year]),
                                )}
                            )

    with tab2:
        # Load GeoJSON file
        geojson_path = 'andy.geojson'
        geojson_data = gpd.read_file(geojson_path)

        # Theme color selection for GeoMap
        color_theme_list = ['Blues', 'cividis', 'Greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.sidebar.selectbox('Pilih tema warna', color_theme_list, key="geo_map_color_theme_selector")

        with st.expander('Desa Maps View Analitycs Clustering', expanded=True):
            create_geomap(df_clustered, geojson_data, selected_color_theme)

        # Moved "SELECT DATA" to the sidebar
        with st.expander("SELECT DATA"):
            selected_city = st.selectbox("Select a city", df_clustered['DESA_1'])
            selected_row = df_clustered[df_clustered['DESA_1'] == selected_city].squeeze()
                # Display additional information in the main area
            st.write("### Selected City Data")
            st.table(selected_row) 
            

               # Graphs
        col1, col2, col3, = st.columns(3)

        with col1:
            with st.container(border=True):
                # Simple line chart showing the count of data points in each cluster
                cluster_counts = df_clustered['cluster'].value_counts().sort_index()
                fig_cluster_counts = px.line(
                    x=cluster_counts.index,
                    y=cluster_counts.values,
                    labels={'x': 'Cluster', 'y': 'Data Point Count'},
                    title='<b>Data Point Count by Cluster</b>',
                    line_shape="linear",
                    render_mode="svg",
                    markers=True
                )
                fig_cluster_counts.update_layout(
                    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
                    paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
                    xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
                    yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
                    font=dict(color='#cecdcd'),  # Set text color to black
                )
                st.plotly_chart(fig_cluster_counts, use_container_width=True)
                
        with col2:
            with st.container(border=True):
                # Create a donut chart
                fig = px.pie(df_clustered, names='cluster', title='Cluster Distribution')
                fig.update_traces(hole=0.4)  # Set the size of the hole in the middle for a donut chart
                fig.update_layout(width=800)
                st.plotly_chart(fig, use_container_width=True)

        with col3:
            with st.container(border=True):
                fig2 = go.Figure(
                    data=[go.Bar(x=df_clustered['cluster'], y=df_clustered[st.session_state.selected_year])],
                    layout=go.Layout(
                        title=go.layout.Title(text=f"Population Distribution by Cluster for {st.session_state.selected_year}"),
                        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
                        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
                        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
                        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
                        font=dict(color='#cecdcd'),  # Set text color to black
                    )
                )

                st.plotly_chart(fig2, use_container_width=True)
                

        with st.expander('KESIMPULAN', expanded=True):
            st.write('''
            **Kesimpulan dari Analisis Agglomerative Hierarchical Clustering (AHC):**

            1. **Pembagian Wilayah Berdasarkan AHC:**
                - Melalui analisis AHC dengan {} klaster dan metode linkage "{}", wilayah berhasil dikelompokkan berdasarkan pola populasi.
                - Klaster tersebut mencerminkan kesamaan karakteristik penduduk di dalamnya.

            2. **Silhouette Score:**
                - Silhouette Score sebesar {} menunjukkan sejauh mana klaster terpisah dan bermakna.
                - Nilai Silhouette Score berkisar antara -1 hingga 1, dengan nilai positif menandakan seberapa baik pengelompokan dilakukan.

            3. **Visualisasi Peta Klaster:**
                - Peta klaster memberikan pandangan visual terhadap sebaran wilayah dalam kelompok-kelompok berbeda.
                - Warna yang berbeda pada peta menunjukkan klaster yang berbeda.

            4. **Tren Penduduk dan Distribusi Klaster:**
                - Grafik garis menunjukkan distribusi data pada setiap klaster.
                - Diagram donat memberikan gambaran proporsi setiap klaster dalam total populasi.
                - Grafik batang menyoroti distribusi populasi pada tahun tertentu di setiap klaster.

            5. **Karakteristik Klaster:**
                - Tabel-tabel data menampilkan rincian populasi dan klaster untuk setiap wilayah.
                - Perbedaan antara wilayah dalam klaster yang berbeda dapat diamati.

            6. **Kesimpulan Tambahan:**
                - AHC membantu dalam mengidentifikasi kesamaan dan perbedaan antara wilayah berdasarkan pola penduduk.
                - Analisis ini dapat menjadi dasar untuk perencanaan pengembangan wilayah.

            7. **Rekomendasi:**
                - Berdasarkan hasil AHC, dapat diambil langkah-langkah strategis untuk pengelolaan dan pengembangan wilayah.

            8. **Catatan Penting:**
                - Penggunaan metode AHC memerlukan pertimbangan parameter dan pemilihan metode linkage yang sesuai.

            Terima kasih telah menggunakan aplikasi ini. Semoga hasil analisis ini bermanfaat untuk pengambilan keputusan dan pengembangan wilayah.
            '''.format(n_clusters, linkage, silhouette_score))
    with tab3:
        col1, col2 = st.columns(2)

        # Prepare silhouette score data for different linkage methods
        silhouette_scores = []
        cluster_range = range(2, 51)
        for method in ['single', 'average', 'complete']:
            scores = []
            for n in cluster_range:
                _, score = ahc_clustering(data_from_homepage, n_clusters=n, linkage=method)
                scores.append(score)
            silhouette_scores.append(scores)

        silhouette_df = pd.DataFrame({
            'Jumlah Cluster': cluster_range,
            'Single Linkage': silhouette_scores[0],
            'Average Linkage': silhouette_scores[1],
            'Complete Linkage': silhouette_scores[2]
        })

        with col1:
            # Display line plot for silhouette scores for different linkage methods
            fig = px.line(
                silhouette_df,
                x='Jumlah Cluster',
                y=['Single Linkage', 'Average Linkage', 'Complete Linkage'],
                labels={'value': 'Silhouette Score', 'variable': 'Metode'},
                title='Silhouette Score untuk Berbagai Jumlah Cluster',
                color_discrete_map={
                    'Single Linkage': 'blue',
                    'Average Linkage': 'green',
                    'Complete Linkage': 'red'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("Choose a specific number of clusters to see details:")
            selected_clusters = st.selectbox("Number of Clusters", cluster_range)
            linkage_method = st.selectbox("Linkage Method", ['single', 'average', 'complete'])
            
            df_selected_clusters, silhouette_selected = ahc_clustering(data_from_homepage, n_clusters=selected_clusters, linkage=linkage_method)
            st.write(f"Silhouette Score for {selected_clusters} clusters using {linkage_method} linkage: {silhouette_selected}")


        


if __name__ == "__main__":
    # Call the ahc_page function
    ahc_page()
