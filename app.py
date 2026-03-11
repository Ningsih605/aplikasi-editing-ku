import streamlit as st
import replicate
import os

st.set_page_config(page_title="Animasi Video AI", page_icon="🎬")

st.title("🎬 Aplikasi Animasi Gambar ke Video")
st.write("Ubah foto diam menjadi video yang bergerak mengikuti video referensimu!")

st.info("Kamu butuh API Token dari replicate.com untuk menjalankan AI ini.")
api_key = st.text_input("🔑 Masukkan Replicate API Token kamu di sini:", type="password")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    source_img = st.file_uploader("1. Upload Foto Wajah Diam (JPG/PNG)", type=["jpg", "jpeg", "png"])
with col2:
    driving_vid = st.file_uploader("2. Upload Video Gerakan (MP4)", type=["mp4"])

if st.button("✨ Buat Video Sekarang!"):
    
    if not api_key:
        st.warning("⚠️ Tolong masukkan API Token Replicate terlebih dahulu!")
    elif source_img is not None and driving_vid is not None:
        
        os.environ["REPLICATE_API_TOKEN"] = api_key
        st.success("File diterima! Sedang mengirim ke AI... Mohon tunggu jangan tutup halaman ini.")
        
        with open("temp_image.jpg", "wb") as f:
            f.write(source_img.getbuffer())
        with open("temp_video.mp4", "wb") as f:
            f.write(driving_vid.getbuffer())
            
        try:
            with st.spinner('AI sedang memproses videomu... Ini butuh waktu beberapa menit ⏳'):
                # KITA GANTI MODEL AI-NYA DI SINI MENGGUNAKAN YANG LEBIH STABIL
                output_video_url = replicate.run(
                    "yoyo-nb/thin-plate-spline-motion-model:212535c5d01439bc0d692880ab6e2f5b823b204e38e658ce5970c7974e64f7b5",
                    input={
                        "source_image": open("temp_image.jpg", "rb"),
                        "driving_video": open("temp_video.mp4", "rb")
                    }
                )
            
            st.balloons()
            st.success("Yeay! Video berhasil dibuat! 🎉")
            st.video(output_video_url)
            
        except Exception as e:
            st.error(f"Yah, terjadi kesalahan. Detail error: {e}")
            
    else:
        st.warning("Mohon upload Foto dan Video referensi terlebih dahulu ya!")
