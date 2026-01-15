from datetime import datetime, timedelta
import mss # Paquete para hacer capturas de pantalla 
import base64 # Paquete para codificar la captura de pantalla

# Caché para la captura de pantalla
screenshot_cache = {
    "image": None,
    "timestamp": None
}

SCREENSHOT_CACHE_DURATION = timedelta(minutes=5)

def get_screenshot():
    # Verificar caché de captura de pantalla
    now = datetime.now()
    cache_expired = (
        screenshot_cache["image"] is None
        or screenshot_cache["timestamp"] is None
        or now - screenshot_cache["timestamp"] > SCREENSHOT_CACHE_DURATION
    )

    if cache_expired:
        # Capturar pantalla, convertir a PNG y codificar en base64
        inst = mss.mss()
        screenshot = inst.grab(inst.monitors[1])  # Monitor principal
        image = base64.b64encode(mss.tools.to_png(screenshot.rgb, screenshot.size)).decode("utf-8")
        inst.close()

        # Guardar en caché la imagen y el tiempo actual
        screenshot_cache["image"] = image
        screenshot_cache["timestamp"] = now
    else:
        # Reutilizar imagen de la caché
        image = screenshot_cache["image"]
    return image

def video_generator():
    # Inicializar captura de pantalla
    sct = mss.mss()
    try:
        # Bucle infinito para capturar continuamente
        while True:
            # Capturar monitor principal
            captura = sct.grab(sct.monitors[1])
            # Convertir a PNG
            png_bytes = mss.tools.to_png(captura.rgb, captura.size)
            # Enviar frame en formato multipart
            yield (b'--frame\r\nContent-Type: image/png\r\n\r\n' + png_bytes + b'\r\n')
    finally:
        # Cerrar captura al desconectar
        sct.close()