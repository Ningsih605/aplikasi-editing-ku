import streamlit as st
import replicate
import os

st.set_page_config(page_title="Animasi Video AI", page_icon="🎬")

st.title("🎬 Aplikasi Animasi Gambar ke Video")
st.write("Ubah foto diam menjadi video yang bergerak mengikuti video referensimu!")

# Meminta user memasukkan API Key secara aman di aplikasi
st.info("Kamu butuh API Token dari replicate.com untuk menjalankan AI ini.")
api_key = st.text_input("🔑 Masukkan Replicate API Token kamu di sini:", type="password")

st.markdown("---")

# Membuat area untuk upload file
col1, col2 = st.columns(2)
with col1:
    source_image = st.file_uploader("1. Upload Foto Wajah Diam (JPG/PNG)", type=["jpg", "jpeg", "png"])
with col2:
    driving_video = st.file_uploader("2. Upload Video Gerakan (MP4)", type=["mp4"])

# Tombol untuk mulai memproses
if st.button("✨ Buat Video Sekarang!"):
    
    # Mengecek apakah API key dan file sudah diisi
    if not api_key:
        st.warning("⚠️ Tolong masukkan API Token Replicate terlebih dahulu!")
    elif source_image is not None and driving_video is not None:
        
        # Mengaktifkan API key
        os.environ["REPLICATE_API_TOKEN"] = api_key
        st.success("File diterima! Sedang mengirim ke AI... Mohon tunggu jangan tutup halaman ini.")
        
        # Menyimpan file sementara
        with open("temp_image.jpg", "wb") as f:
            f.write(source_image.getbuffer())
        with open("temp_video.mp4", "wb") as f:
            f.write(driving_video.getbuffer())
            
        try:
            with st.spinner('AI sedang melukis videomu... Proses ini bisa memakan waktu 1-3 menit ⏳'):
                # Mengirim ke server AI Replicate
                output_video_url = replicate.run(
                    "fofr/live-portrait:53554e20173e6ebaa04de66c9f223126ed314d3ee124319fb77bc40497d39c94",
                    input={
                        "image": open("temp_image.jpg", "rb"),
                        "video": open("temp_video.mp4", "rb")
                    }
                )
            
            # Menampilkan hasil
            st.balloons()
            st.success("Yeay! Video berhasil dibuat! 🎉")
            st.video(output_video_url)
            
        except Exception as e:
            st.error(f"Yah, terjadi kesalahan. Pastikan API Token benar. Detail error: {e}")
            
    else:
        st.warning("Mohon upload Foto dan Video referensi terlebih dahulu ya!")
