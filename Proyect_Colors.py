import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

def main():
    st.set_page_config(page_title="Gotero de Colores", layout="wide")
    st.title("🎨 Gotero de Colores en Streamlit")

    # Selección de función
    option = st.sidebar.selectbox("Selecciona una función", ["Subir Imagen", "Abrir Cámara"])

    if option == "Subir Imagen":
        uploaded_file = st.file_uploader("📂 Sube una imagen (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            # Cargar la imagen
            image = Image.open(uploaded_file).convert("RGB")

            # Zoom interactivo
            zoom_level = st.slider("🔍 Nivel de Zoom", 0.5, 3.0, 1.0, 0.1)
            zoomed_image = image.resize((int(image.width * zoom_level), int(image.height * zoom_level)))

            # Canvas interactivo para clics
            st.subheader("📍 Haz clic sobre la imagen para seleccionar un color:")
            canvas_result = st_canvas(
                fill_color="rgba(0, 0, 0, 0)",  # No se usa relleno
                stroke_width=1,
                background_image=zoomed_image,
                height=int(zoomed_image.height),
                width=int(zoomed_image.width),
                drawing_mode="freedraw",
                key="canvas",
            )

            # Obtener coordenadas del clic y color seleccionado
            if canvas_result.json_data:
                try:
                    x, y = canvas_result.json_data["objects"][-1]["left"], canvas_result.json_data["objects"][-1]["top"]
                    x, y = int(x / zoom_level), int(y / zoom_level)  # Ajustar al nivel de zoom
                    rgb_color = image.getpixel((x, y))
                    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
                    text_color = "black" if sum(rgb_color) / 3 > 200 else "white"

                    st.markdown(
                        f"""
                        <div style="background-color:{hex_color}; color:{text_color}; padding:10px; border-radius:10px;">
                            <b>Color seleccionado:</b><br>
                            RGB: {rgb_color}<br>
                            Hex: {hex_color}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error("Haz clic dentro de los límites de la imagen.")

    elif option == "Abrir Cámara":
        st.subheader("📷 Cámara en Vivo")
        run_camera = st.checkbox("Activar Cámara")

        if run_camera:
            # Usa el widget de carga de archivo de video
            video_file = st.camera_input("Captura una imagen con tu cámara")

            if video_file:
                # Leer el archivo de video como imagen
                image = Image.open(video_file).convert("RGB")
                st.image(image, caption="Imagen capturada", use_column_width=True)

                # Selección de color (mismo proceso que con imagen cargada)
                st.subheader("📍 Haz clic sobre la imagen para seleccionar un color:")
                canvas_result = st_canvas(
                    fill_color="rgba(0, 0, 0, 0)",
                    stroke_width=1,
                    background_image=image,
                    height=image.height,
                    width=image.width,
                    drawing_mode="freedraw",
                    key="canvas_camera",
                )

                if canvas_result.json_data:
                    try:
                        x, y = canvas_result.json_data["objects"][-1]["left"], canvas_result.json_data["objects"][-1]["top"]
                        rgb_color = image.getpixel((int(x), int(y)))
                        hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
                        text_color = "black" if sum(rgb_color) / 3 > 200 else "white"

                        st.markdown(
                            f"""
                            <div style="background-color:{hex_color}; color:{text_color}; padding:10px; border-radius:10px;">
                                <b>Color seleccionado:</b><br>
                                RGB: {rgb_color}<br>
                                Hex: {hex_color}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error("Haz clic dentro de los límites de la imagen.")

if __name__ == "__main__":
    main()
