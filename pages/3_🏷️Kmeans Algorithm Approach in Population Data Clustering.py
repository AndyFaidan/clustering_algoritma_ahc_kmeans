import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import silhouette_score
import time


st.set_page_config(
    page_title="Kmeans Algorithm Approach in Population Data Clustering",
    page_icon="📊",
    layout="wide",  # Set layout to wide for full-width content
    initial_sidebar_state="collapsed",  # Collapse the sidebar by default
) 


def kmeans_clustering(data, num_clusters, selected_year):
    # Select columns for clustering
    features = data[['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']]
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(features)
    
    # Calculate centroid for each cluster
    centroids = data.groupby('cluster')[['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']].mean()

    # Define threshold values for density categories (adjust these based on your analysis)
    threshold_low = 10000  # Example threshold for "not dense"
    threshold_high = 50000  # Example threshold for "dense"

    # Add Density Category column based on centroid values
    data['Density Category'] = data['cluster'].map(lambda cluster: 'Tidak Padat' if centroids.loc[cluster].mean() < threshold_low else ('Padat' if centroids.loc[cluster].mean() < threshold_high else 'Sangat Padat'))
    
    # Elbow Method data
    elbow_data = pd.DataFrame({'num_clusters': range(1, 11),
                               'inertia': [KMeans(n_clusters=i, random_state=42).fit(features).inertia_ for i in range(1, 11)]})
    # Calculate Silhouette Score
    silhouette_avg = silhouette_score(features, data['cluster'])

    return data, silhouette_avg, elbow_data



# Function to display Silhouette Progress Bar
def SilhouetteProgressBar(silhouette_avg, target):
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)

    current = silhouette_avg
    percent = round((current / target * 100))
    mybar = st.progress(0)

    if percent >= 100:
        st.subheader("Target silhouette score achieved!")
    else:
        st.write("Current silhouette score: {:.2f}".format(current))
        st.write("You have {:.2f}% of the target silhouette score".format(percent))

        for percent_complete in range(percent):
            time.sleep(1)
            mybar.progress(percent_complete + 1, text="Silhouette Score Percentage")
    
# Function to create GeoMap with Plotly Express
def create_geomap(data, geojson_data, selected_color_theme):
    # Merge GeoJSON data with clustered data based on 'DESA_1'
    merged_data = geojson_data.merge(data, left_on='DESA_1', right_on='DESA_1')

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
    # Set the map to full-width
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    # Show the GeoMap
    st.plotly_chart(fig, use_container_width=True)

def kmeans_page():
    center = True
    st.header("KMeans Clustering Page", anchor='center' if center else 'left')
    st.latex(r"SSE = \sum_{i=1}^{k} \sum_{j=1}^{n} ||x_{ij} - c_i||^2")

    # Sidebar: Choose the number of clusters
    num_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=3)

    # Select Year in the Sidebar
    st.sidebar.title("Select Year")
    selected_year = st.sidebar.selectbox('Select Year', ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])

    # Load data from the home page
    data_from_homepage = pd.read_csv('Data_Original_Update.csv')  # Replace with your actual data

    # Perform KMeans clustering
    df_clustered, silhouette_avg, elbow_data = kmeans_clustering(data_from_homepage, num_clusters, selected_year)

    # Save the clustered data and elbow data in session_state
    st.session_state.df_clustered = df_clustered
    st.session_state.elbow_data = elbow_data

    tab1, tab2 = st.tabs(["DATASET", "VISUALISASI MAP"])

    with tab1:
        # Progress bar for Silhouette Score
        SilhouetteProgressBar(silhouette_avg, target=1.0)


        # Display metrics for each cluster
        for cluster_num in range(num_clusters):
            # Get the density category for the current cluster
            density_category = df_clustered.loc[df_clustered['cluster'] == cluster_num, 'Density Category'].iloc[0]

            cluster_data = df_clustered[df_clustered['cluster'] == cluster_num][["DESA_1", "cluster", selected_year]]

            with st.expander(f"Cluster {cluster_num + 1} Data Table - {density_category}", expanded=True):
                st.dataframe(cluster_data,
                            column_order=("DESA_1", selected_year, "cluster"),
                            hide_index=True,
                            width=500,
                            use_container_width=True,
                            column_config={
                                "DESA_1": st.column_config.TextColumn(
                                    "Area",
                                ),
                                selected_year: st.column_config.ProgressColumn(
                                    selected_year,
                                    format="%f",
                                    min_value=0,
                                    max_value=max(cluster_data[selected_year]),
                                )}
                            )

    with tab2:
        # Load GeoJSON file
        geojson_path = 'andy.geojson'
        geojson_data = gpd.read_file(geojson_path)

        # Theme color selection for GeoMap
        st.sidebar.title("GeoMap Color Theme Selection")
        color_theme_list = ['Blues', 'cividis', 'Greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.sidebar.selectbox('Pilih tema warna', color_theme_list, key="geo_map_color_theme_selector")
        
        with st.container(border=True):
            create_geomap(df_clustered, geojson_data, selected_color_theme)

            # Show table data when hovering over a marker
        with st.expander("SELECT DATA"):
            selected_city = st.selectbox("Select ", df_clustered['DESA_1'])
            selected_row = df_clustered[df_clustered['DESA_1'] == selected_city].squeeze()
            # Display additional information in a table
            st.table(selected_row)

                    # Graphs
        col1, col2, col3, col4 = st.columns(4)

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
                    data=[go.Bar(x=df_clustered['cluster'], y=df_clustered[selected_year])],
                    layout=go.Layout(
                        title=go.layout.Title(text=f"Population Distribution by Cluster for {selected_year}"),
                        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
                        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
                        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
                        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
                        font=dict(color='#cecdcd'),  # Set text color to black
                    )
                )
                st.plotly_chart(fig2, use_container_width=True)

        with col4:
            with st.container(border=True):
                    # Elbow Method Line Chart
                    fig_elbow = px.line(elbow_data, x='num_clusters', y='inertia', markers=True, title='Elbow Method',
                                        labels={'num_clusters': 'Number of Clusters', 'inertia': 'Inertia'})
                    fig_elbow.update_layout(
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
                        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
                        font=dict(color='#cecdcd'),
                    )
                    st.plotly_chart(fig_elbow, use_container_width=True)

        with st.expander('kesimpulan', expanded=True):
                st.write('''
                1. **Pembagian Wilayah Berdasarkan KMeans:**
                    - Berdasarkan analisis KMeans dengan {} klaster, wilayah telah terbagi ke dalam kelompok-kelompok dengan pola-pola tertentu.
                    - Klaster dapat membantu memahami karakteristik penduduk setiap wilayah.

                2. **Visualisasi Peta Klaster:**
                    - Peta klaster memberikan pandangan visual terhadap sebaran wilayah dalam kelompok-kelompok tertentu.
                    - Wilayah dengan warna yang sama menunjukkan kemiripan karakteristik penduduk.

                3. **Tren Penduduk:**
                    - Grafik garis menunjukkan distribusi data pada setiap klaster.
                    - Diagram donat memberikan gambaran proporsi setiap klaster dalam total populasi.
                    - Grafik batang menyoroti distribusi populasi pada tahun tertentu di setiap klaster.

                4. **Karakteristik Klaster:**
                    - Tabel-tabel data menampilkan rincian populasi dan klaster untuk setiap wilayah.
                    - Dapat dilihat perbedaan antara wilayah yang termasuk dalam klaster yang berbeda.

                5. **Kesimpulan Tambahan:**
                    - Dengan menggunakan metode KMeans, kami dapat mengelompokkan wilayah berdasarkan pola populasi.
                    - Identifikasi wilayah dengan tingkat kepadatan populasi yang berbeda membantu dalam perencanaan dan pengambilan keputusan.

                6. **Rekomendasi:**
                    - Berdasarkan hasil analisis, dapat diambil keputusan dan langkah-langkah strategis untuk pengembangan dan perbaikan di berbagai wilayah.

                7. **Catatan Penting:**
                    - Silhouette Score sebesar {} menunjukkan sejauh mana klaster terpisah dan bermakna.
                    - Penggunaan metode ini dapat disesuaikan dengan penyesuaian parameter dan pemilihan fitur yang lebih baik.

                Terima kasih telah menggunakan aplikasi ini. Semoga hasil analisis ini memberikan wawasan yang berguna untuk pengambilan keputusan.
                '''.format(num_clusters, silhouette_avg))


if __name__ == "__main__":
    # Call the kmeans_page function
    kmeans_page()
