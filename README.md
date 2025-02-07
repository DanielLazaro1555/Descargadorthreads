# 📥 Descargador de Videos e Imágenes de Threads

Un **descargador de videos e imágenes** de **Threads** construido con **FastAPI, Selenium y React.js**. Permite extraer contenido en alta calidad y descargarlo fácilmente.

---

## 🚀 Características

✅ **Descarga videos e imágenes en alta calidad** desde Threads.  
✅ **Interfaz moderna y responsive** con **React y Bootstrap**.  
✅ **Conversión automática de imágenes a PNG sin pérdida de calidad**.  
✅ **Soporte para múltiples imágenes y videos en un solo post**.  
✅ **Uso de Selenium** para extraer contenido dinámico.  
✅ **Preparado para despliegue en la nube con Docker y Render**.

---

## 🛠️ Tecnologías Utilizadas

- **Frontend**: React.js, Bootstrap, JavaScript (ES6+)
- **Backend**: FastAPI, Python, Selenium, Requests
- **Infraestructura**: Docker, Render (Cloud Deployment)

---

## 🔧 Instalación y Ejecución

### **1️⃣ Clonar el repositorio**

```bash
git clone https://github.com/TU_USUARIO/DescargadorThreads.git
cd DescargadorThreads
```

2️⃣ Configurar el backend (FastAPI + Selenium)

    Instalar dependencias:

pip install -r requirements.txt

Descargar y colocar geckodriver en /usr/local/bin/
🔗 Descargar geckodriver aquí

Ejecutar FastAPI:

uvicorn app:app --reload

Esto iniciará el backend en http://127.0.0.1:8000

3️⃣ Configurar el frontend (React)

    Ir a la carpeta del frontend:

cd frontend

Instalar dependencias:

npm install

Ejecutar React:

npm start

Esto iniciará el frontend en http://localhost:3000

📸 Capturas de Pantalla

📌 Ejemplo de Descarga de Video

📄 API Endpoints (FastAPI)
1️⃣ Obtener contenido multimedia de Threads

GET /get_media?url={URL_DE_THREADS}

📌 Ejemplo de respuesta:

{
  "images": ["![Captura de Ejemplo](Captura%20desde%202025-02-07%2015-35-36.png)"]
}


2️⃣ Descargar archivo

GET /downloads/{filename}

🎯 Mejoras Futuras

Agregar soporte para múltiples hilos en una sola descarga.
Implementar una barra de progreso para las descargas.
Mejorar el procesamiento de imágenes en segundo plano.

⭐ Si te gusta este proyecto, dale una estrella ⭐

---

## **📌 ¿Qué incluye este README?**

✅ **Descripción clara del proyecto**  
✅ **Tecnologías utilizadas**  
✅ **Guía de instalación (Backend + Frontend)**  
✅ **Ejemplos de uso con API y Docker**  
✅ **Capturas de pantalla** _(puedes subir imágenes reales y actualizar los links)_  
✅ **Mejoras futuras y contribuciones**


🔗 Licencia MIT

Este proyecto está licenciado bajo la Licencia MIT, lo que significa que puedes usarlo, modificarlo y compartirlo libremente.

📜 Licencia: MIT License