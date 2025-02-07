from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from fastapi.responses import FileResponse
import requests
import os
import time

# Inicializar FastAPI
app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta para guardar imágenes descargadas
UPLOAD_FOLDER = "downloads"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)  # Crear carpeta si no existe


def scroll_until_all_images_loaded(driver):
    """ Hace scroll hasta que no haya nuevas imágenes en la página. """
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_images_count = 0

    for _ in range(15):  # Intentar hasta 15 veces para asegurarnos de que bajamos todo
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Esperar que se carguen las imágenes

        # Contar imágenes después de cada scroll
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        new_images_count = len(img_elements)

        print(f"🔍 Detectadas {new_images_count} imágenes después del scroll")

        # Si ya no hay más imágenes nuevas, detener el scroll
        if new_images_count == last_images_count:
            print("✅ No hay más imágenes nuevas, terminando scroll")
            break

        last_images_count = new_images_count  # Actualizar el número de imágenes
        last_height = driver.execute_script(
            "return document.body.scrollHeight")


def get_media_url(thread_url):
    """ Usa Selenium para obtener la URL de todos los videos e imágenes en alta calidad. """
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Modo sin interfaz gráfica
    options.add_argument("--disable-gpu")

    service = Service("/usr/local/bin/geckodriver")  # Ruta a geckodriver
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(thread_url)
        time.sleep(5)  # Esperar carga inicial

        # Hacer scroll profundo hasta cargar todas las imágenes
        scroll_until_all_images_loaded(driver)

        # Encontrar todos los videos
        video_elements = driver.find_elements(By.TAG_NAME, "video")
        videos = [video.get_attribute("src") for video in video_elements if video.get_attribute(
            "src") and video.get_attribute("src").startswith("https://scontent")]

        # Encontrar todas las imágenes en alta calidad
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        images = [img.get_attribute("src") for img in img_elements if img.get_attribute(
            "alt") and "Photo" in img.get_attribute("alt") and img.get_attribute("src").startswith("https://scontent")]

        print(f"✅ {len(videos)} VIDEOS ENCONTRADOS")
        print(f"✅ {len(images)} IMÁGENES ENCONTRADAS")

        # Si no se encontró nada, devolver error
        if not videos and not images:
            raise HTTPException(
                status_code=404, detail="No se pudo obtener videos ni imágenes en alta calidad.")

        return {"videos": videos, "images": images}

    finally:
        driver.quit()  # Cerrar el navegador


@app.get("/get_media")
def get_media(url: str):
    """ Descarga todas las imágenes si es necesario y devuelve listas separadas de videos e imágenes. """
    try:
        media = get_media_url(url)  # Obtener URLs reales de contenido
        local_images = []

        # Descargar imágenes y servirlas localmente
        for img_url in media["images"]:
            img_filename = img_url.split("/")[-1].split("?")[0]
            img_path = f"{UPLOAD_FOLDER}/{img_filename}"

            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                with open(img_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                local_images.append(
                    f"http://127.0.0.1:8000/downloads/{img_filename}")

        return {
            "videos": media["videos"],
            "images": local_images  # Servimos imágenes desde el backend
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/downloads/{filename}")
def serve_file(filename: str):
    """ Sirve los archivos guardados en el backend """
    file_path = f"{UPLOAD_FOLDER}/{filename}"
    if Path(file_path).exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Archivo no encontrado")
