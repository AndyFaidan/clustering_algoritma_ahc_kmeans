import streamlit as st
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide") 


# Define a function for the tooltip (if needed)
def tooltip(image_url, text):
    return f'<img src="{image_url}" title="{text}" style="border: 1px solid blue; border-radius:4px; background-color:green; color: white; padding:2px;">'

# HTML content
html_content = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <style>
    iframe {{
        margin-bottom: 0px;
    }}
    html {{
        margin-top: 0px;
        margin-bottom: 0px;
        border: 1px solid #de3f53; padding:0px 4px;
        font-family: "Source Sans Pro", sans-serif;
        font-weight: 400;
        line-height: 1.6;
        color: rgb(49, 51, 63);
        background-color: rgb(255, 255, 255);
        text-size-adjust: 100%;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-font-smoothing: auto;
    }}
    </style>

    <h2 style='color: #de3f53; margin-top:0px; border-bottom: solid 5px;'>Tentang Analisis Klaster AHC dan K-Means pada Data BPS Kabupaten Purwakarta</h2>
"""

# Display the HTML content
st.markdown(html_content, unsafe_allow_html=True)

# Menambahkan jarak
st.markdown("&nbsp;", unsafe_allow_html=True)  # Spasi menggunakan HTML entity


 # Deskripsi menggunakan markdown
st.success('''
        **Pendahuluan: 📊**
        Pertumbuhan penduduk yang dipengaruhi oleh faktor alam, migrasi, dan kebijakan menjadikan Kabupaten Purwakarta, Jawa Barat, sebagai Kota Metropolitan pada tahun 2023 dengan jumlah penduduk 1.028.569 jiwa dan luas wilayah 971,72 km². Kepadatan penduduk mencerminkan distribusi penduduk di wilayah tersebut. Pertumbuhan tahunan mencapai 15.774 jiwa (1,52%), dengan Kecamatan Campaka memiliki pertumbuhan tertinggi (2,92%) dan Kecamatan Purwakarta terendah (0,71%).
        Peningkatan jumlah penduduk di Purwakarta meningkatkan kepadatan, berpotensi memicu kriminalitas dan degradasi ekosistem. Pertumbuhan cepat ini menambah kebutuhan pangan, air bersih, dan tempat tinggal, serta meningkatkan risiko pencemaran air, tanah, dan udara. Ketidakseimbangan antara sumber daya alam dan kebutuhan manusia menyebabkan penurunan sumber daya dan hilangnya keanekaragaman hayati.
       
        **Pendekatan Utama: 🌐**

        1. **Agglomerative Hierarchical Clustering (AHC):**
            - AHC adalah metode klaster hierarkis yang secara iteratif menggabungkan titik data yang mirip ke dalam klaster.
            - Analisis ini bertujuan untuk mengungkap struktur alami dalam data demografis, mengidentifikasi kelompok wilayah dengan karakteristik populasi yang serupa.

        2. **K-Means Clustering:**
            - K-Means membagi data menjadi 'k' klaster berdasarkan kemiripan.
            - Dengan menerapkan K-Means bertujuan untuk mengelompokkan objek/data ke dalam cluster yang memiliki karakteristik yang sama.

        **Sumber Data: 📈**

        Data penduduk yang digunakan dalam analisis ini berasal dari Badan Pusat Statistik (BPS) Kabupaten Purwakarta dari website purwakartakab.bps.go.id.
        Data ini mencakup atribut:
        Desa, tahun, dan jumlah penduduk. Data tersebut mencakup Desa/Kelurahan di setiap Kecamatan di Kabupaten Purwakarta dan diambil dari tahun 2011 hingga 2023.

        **Tujuan: 🎯**

        Tujuan utama adalah solusi pemerintah Kabupaten Purwakarta untuk pengambilan keputusan terkait kebijakan, program, atau proyek yang berhubungan dengan penduduk juga dalam mengambil keputusan yang lebih tepat dan efisien untuk kepentingan masyarakat dengan pembagian cluster tingkat kepadatan tidak padat, padat dan sangat padat.

   
        **Pendekatan Metodologis: 📊**

        Metode AHC digunakan untuk mengeksplorasi struktur hierarkis dalam data demografis, sementara K-Means memberikan pemahaman tentang kelompok populasi yang lebih terdefinisi. Kombinasi kedua metode ini memberikan pandangan holistik tentang distribusi dan hubungan antarwilayah.

        **Kesimpulan: 🌟**

        Analisis klaster dengan AHC dan K-Means diharapkan dapat memberikan gambaran yang lebih dalam tentang populasi Kabupaten Purwakarta. Hasilnya dapat digunakan sebagai dasar untuk kebijakan pembangunan yang lebih efektif, memastikan bahwa sumber daya dialokasikan dengan bijak sesuai dengan kebutuhan unik setiap wilayah.
    ''')
 
st.info('''
        Hasil analisis klaster menggunakan metode Agglomerative Hierarchical Clustering (AHC) dan K-Means pada data demografis BPS Kabupaten Purwakarta dapat memberikan wawasan yang berharga untuk:

            * **Mengidentifikasi** pola dan kelompok dalam populasi.
            * **Mendukung** pengambilan keputusan yang terinformasi.
            * **Mengarahkan** intervensi dengan lebih tepat.

            Analisis ini dapat menjadi **alat penting** bagi **pembuat kebijakan**, **peneliti**, dan **otoritas lokal** dalam:

            * **Memahami** keragaman dalam wilayah tersebut.
            * **Merancang** strategi pembangunan yang sesuai.

            Dengan menggunakan teknik klaster seperti AHC dan K-Means, kita dapat mengeksplorasi struktur alami dalam data demografis, mengidentifikasi kelompok wilayah dengan karakteristik populasi yang serupa, dan menemukan cluster populasi yang berbeda.

            Analisis ini memberikan landasan untuk **menginformasikan** kebijakan pembangunan wilayah dan **mengeksplorasi** faktor-faktor yang dapat mempengaruhi pola demografis di Kabupaten Purwakarta.
            ''', icon="🧐")

with st.container(border=True):
        st.markdown("""
        Berikut adalah video YouTube yang menjelaskan tentang K-Means Clustering. Anda dapat menonton video ini langsung di YouTube untuk mendapatkan pemahaman yang lebih baik tentang metode tersebut.
        """)

        # Embed YouTube video
        video_url_kmeans = "https://www.youtube.com/embed/BMzXuG1p3lQ?t=887s"
        video_html_kmeans = f"""
            <div style="display: flex; justify-content: center;">
                <iframe width="1000" height="450" src="{video_url_kmeans}" 
                frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
                </iframe>
            </div>
        """
        components.html(video_html_kmeans, height=450)
        
with st.container(border=True):
        # Judul dan deskripsi
        st.markdown("""
        Berikut adalah video YouTube yang menjelaskan tentang Agglomerative Hierarchical Clustering (AHC). Anda dapat menonton video ini langsung di YouTube untuk mendapatkan pemahaman yang lebih baik tentang metode tersebut.
        """)

        # Embed YouTube video
        video_url_ahc = "https://www.youtube.com/embed/s8K0lO9OFOA?start=1067"
        video_html_ahc = f"""
            <div style="display: flex; justify-content: center;">
                <iframe width="1000" height="450" src="{video_url_ahc}" 
                frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
                </iframe>
            </div>
        """
        components.html(video_html_ahc, height=450)


