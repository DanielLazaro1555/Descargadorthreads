import React, { useState } from "react";

const DownloadForm = () => {
  const [url, setUrl] = useState("");
  const [videos, setVideos] = useState([]);
  const [images, setImages] = useState([]);
  const [message, setMessage] = useState("");

  const handleGetMedia = async () => {
    if (!url) {
      setMessage("❌ Ingresa un enlace válido.");
      return;
    }

    // Limpiar contenido anterior
    setVideos([]);
    setImages([]);
    setMessage("⏳ Cargando contenido...");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/get_media?url=${encodeURIComponent(url)}`
      );
      const data = await response.json();

      if (response.ok) {
        setVideos(data.videos || []);
        setImages(data.images || []);
        setMessage("");
      } else {
        setMessage(`❌ Error: ${data.detail}`);
        setVideos([]);
        setImages([]);
      }
    } catch (error) {
      setMessage("❌ Hubo un problema al obtener el contenido.");
      setVideos([]);
      setImages([]);
    }
  };

  const handleDownload = (imageUrl) => {
    if (!imageUrl) {
        console.error("❌ Error: No se proporcionó una URL de imagen.");
        return;
    }

    // Obtener el nombre del archivo desde la URL
    const filename = imageUrl.split("/").pop().split("?")[0] || "imagen.png";

    // Crear una imagen temporal
    const img = new Image();
    img.crossOrigin = "anonymous"; // Para evitar problemas de CORS
    img.src = imageUrl;

    img.onload = () => {
        // Crear un canvas del tamaño de la imagen
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

        canvas.width = img.width;
        canvas.height = img.height;

        // Dibujar la imagen en el canvas
        ctx.drawImage(img, 0, 0, img.width, img.height);

        // Convertir a PNG y descargar
        const pngUrl = canvas.toDataURL("image/png"); // Guardar en formato PNG
        const link = document.createElement("a");
        link.href = pngUrl;
        link.download = filename.replace(".jpg", ".png"); // Cambiar extensión a .png
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    img.onerror = () => {
        console.error("❌ Error al cargar la imagen para conversión.");
    };
};


  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <h2 className="text-center">
          <span role="img" aria-label="icon">
            📥
          </span>{" "}
          Descargar de Threads
        </h2>

        {/* Campo de entrada */}
        <input
          type="text"
          className="form-control my-3"
          placeholder="Pega aquí el enlace del post de Threads"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        {/* Botón para obtener contenido */}
        <button className="btn btn-primary w-100" onClick={handleGetMedia}>
          <span role="img" aria-label="search">
            🔍
          </span>{" "}
          Obtener Contenido
        </button>

        {/* Mensaje de estado */}
        {message && <p className="mt-3 text-center">{message}</p>}

        {/* Sección de previsualización en cuadrícula */}
        {(videos.length > 0 || images.length > 0) && (
          <div className="mt-4">
            <h5>🖼️ Contenido Descargable:</h5>

            <div className="row">
              {/* Mostrar videos */}
              {videos.map((video, index) => (
                <div key={index} className="col-md-3">
                  <div className="card shadow mb-4">
                    <video className="card-img-top" controls>
                      <source src={video} type="video/mp4" />
                      Tu navegador no soporta el formato de video.
                    </video>
                    <div className="card-body text-center">
                      <button
                        className="btn btn-success"
                        onClick={() => handleDownload(video)}
                      >
                        📥 Descargar
                      </button>
                    </div>
                  </div>
                </div>
              ))}

              {/* Mostrar imágenes */}
              {images.map((img, index) => (
                <div key={index} className="col-md-3">
                  <div className="card shadow mb-4">
                    <img
                      src={img}
                      className="card-img-top"
                      alt={`Imagen ${index + 1}`}
                    />
                    <div className="card-body text-center">
                      <button
                        className="btn btn-success"
                        onClick={() => handleDownload(img)}
                      >
                        📥 Descargar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DownloadForm;
