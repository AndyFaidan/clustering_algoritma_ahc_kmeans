import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="Analisis Clustering Kepadatan Penduduk",
    layout="wide",  # Set layout to wide for full-width content
    initial_sidebar_state="collapsed",  # Collapse the sidebar by default
)

def homepage():
    st.header("Home Page")

alt.themes.enable("dark")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Memuat file GeoJSON
geojson_file = 'andy.geojson'
gdf_geojson = gpd.read_file(geojson_file)

# Memuat file CSV, set kolom 'Unnamed: 0' sebagai indeks
csv_file = 'AUDIT_data_kab.pwk.csv'
df_csv = pd.read_csv(csv_file, index_col=0)

# Menggabungkan dataset berdasarkan DESA_1
merged_df = gdf_geojson.merge(df_csv, how='left', left_on='DESA_1', right_on='DESA_1')

# Mengubah bentuk DataFrame jika diperlukan
df_reshaped = df_csv.groupby(['year', 'DESA_1']).agg({'population': 'sum'}).reset_index()

# Aplikasi Streamlit
st.title('Visualisasi Distribusi Penduduk')

# Sidebar untuk pemilihan tahun
selected_year = st.sidebar.slider('Pilih Tahun', min_value=df_csv['year'].min(), max_value=df_csv['year'].max(), value=df_csv['year'].min())

# Pemilihan tema warna
color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
selected_color_theme = st.sidebar.selectbox('Pilih tema warna', color_theme_list)


# Memfilter data untuk tahun yang dipilih
filtered_df = merged_df[['DESA_1', 'geometry', 'year', 'population']].loc[merged_df['year'] == selected_year]

# Menghitung pusat dan zoom berdasarkan bounding box geometri yang dipilih
center_lat, center_lon = filtered_df.geometry.centroid.y.mean(), filtered_df.geometry.centroid.x.mean()
zoom = 8.5  # Sesuaikan tingkat zoom

# Membuat peta interaktif menggunakan Plotly Express
fig = px.choropleth_mapbox(
    filtered_df,
    geojson=filtered_df.geometry,
    locations=filtered_df.index,
    color='population',
    hover_name='DESA_1',
    mapbox_style="carto-darkmatter",
    center={"lat": center_lat, "lon": center_lon},
    zoom=zoom,
    color_continuous_scale=selected_color_theme,
    range_color=(min(filtered_df['population']), max(filtered_df['population']))
)

# Menetapkan tata letak peta
fig.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    margin=dict(l=0, r=0, t=0, b=0),
    height=400  # Sesuaikan tinggi
)

# Fungsi heatmap dengan pemilihan tema warna
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Tahun", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'{input_color}:Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=500  # Sesuaikan lebar
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Fungsi konversi populasi ke teks
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} Jt'
        return f'{round(num / 1000000, 1)} Jt'
    return f'{num // 1000} K'

# Fungsi perhitungan migrasi penduduk tahun ke tahun
def calculate_population_difference(input_df, input_year):
    selected_year_data = input_df[input_df['year'] == input_year].reset_index()
    previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
    selected_year_data['population_difference'] = selected_year_data['population'].sub(previous_year_data['population'], fill_value=0)
    return pd.concat([selected_year_data['DESA_1'], selected_year_data['year'], selected_year_data['population'], selected_year_data['population_difference']], axis=1).sort_values(by="population_difference", ascending=False)

# Panel Utama Dashboard
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    #st.markdown('#### Kenaikan/Penurunan')

    df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

    if selected_year > 2010:
        first_state_name = df_population_difference_sorted['DESA_1'].iloc[0]
        first_state_population = format_number(int(df_population_difference_sorted['population'].iloc[0]))
        first_state_delta = format_number(int(df_population_difference_sorted['population_difference'].iloc[0]))
    else:
        first_state_name = '-'
        first_state_population = '-'
        first_state_delta = ''
    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    if selected_year > 2010:
        last_state_name = df_population_difference_sorted['DESA_1'].iloc[-1]
        last_state_population = format_number(int(df_population_difference_sorted['population'].iloc[-1]))   
        last_state_delta = format_number(int(df_population_difference_sorted['population_difference'].iloc[-1]))   
    else:
        last_state_name = '-'
        last_state_population = '-'
        last_state_delta = ''
    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    if selected_year > 2010:
        total_population_selected_year = df_reshaped[df_reshaped['year'] == selected_year]['population'].sum()
        total_population_last_year = df_reshaped[df_reshaped['year'] == selected_year - 1]['population'].sum()
        population_difference = total_population_selected_year - total_population_last_year

        total_population_name = "Total Populasi"
        total_population_value = format_number(total_population_selected_year)
        total_population_delta = format_number(population_difference) if population_difference != 0 else "0"

        st.metric(label=total_population_name, value=total_population_value, delta=total_population_delta)
    else:
        st.metric(label="-", value="-", delta="")



with col[1]:
       #st.markdown('#### Total Population')

    # Display the interactive map
    st.plotly_chart(fig, use_container_width=True)

    # Assuming 'geometry' column needs to be excluded
    merged_df_no_geom = merged_df.drop(columns=['geometry'])

with col[2]:
    #st.markdown('#### Top Areas')

    # Sort and filter data
    df_population_sorted = filtered_df.sort_values(by="population", ascending=False)

    # Exclude the 'geometry' column when displaying the GeoDataFrame
    df_population_sorted_no_geom = df_population_sorted.drop(columns=['geometry'])

    st.dataframe(df_population_sorted_no_geom,
                 column_order=("DESA_1", "population"),
                 hide_index=True,
                 width=500,
                 column_config={
                     "DESA_1": st.column_config.TextColumn(
                         "Area",
                     ),
                     "population": st.column_config.ProgressColumn(
                         "Population",
                         format="%f",
                         min_value=0,
                         max_value=max(df_population_sorted.population),
                     )}
                 )


with st.expander("HeatMap", expanded=False):
    st.markdown('#### HeatMap')

    # Mengasumsikan selected_color_theme adalah variabel yang menyimpan tema warna yang diinginkan
    heatmap_chart = make_heatmap(merged_df_no_geom, 'year', 'DESA_1', 'population', selected_color_theme)

    st.altair_chart(heatmap_chart, use_container_width=True)

with st.expander('Informasi', expanded=True):
    st.info(f'''
        - Data: [Data Penduduk Kabupaten Purwakarta](your_data_source_link).
        - :orange[**Area Teratas berdasarkan Penduduk**]: Area dengan penduduk tertinggi untuk tahun {selected_year}.
        - :orange[**Perubahan Penduduk Ekstrem**]: Area dengan peningkatan dan penurunan penduduk terbesar dari tahun sebelumnya ({selected_year - 1} ke {selected_year}).
        - :information_source: **Rata-rata Penduduk ({selected_year}):** {merged_df[merged_df['year'] == selected_year]['population'].mean():,.0f}
        - :information_source: **Rata-rata Penduduk (Area Teratas, {selected_year}):** {filtered_df['population'].mean():,.0f}
        - :information_source: **Modus Penduduk (Area Teratas, {selected_year}):** {filtered_df['population'].mode()[0]:,.0f}
        - :bar_chart: **Visualisasi Penduduk:** Peta korelasi dan peta panas menampilkan total penduduk di berbagai area untuk tahun {selected_year}.
        - :chart_with_upwards_trend: **Tren Penduduk:** Kenaikan/Penurunan, Area Teratas/Terendah berdasarkan Penduduk, dan Perubahan Penduduk Ekstrem divisualisasikan untuk memberikan wawasan tentang dinamika penduduk pada tahun {selected_year}.
    ''')


if __name__ == "__main__":
    # Call the homepage function
    data_from_homepage = homepage()
