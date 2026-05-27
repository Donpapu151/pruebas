import requests
import random
import xml.etree.ElementTree as ET

# 📊 CONFIGURACIÓN DE TU CANAL:
URL_DISCORD_FNAF = "https://discord.com/api/webhooks/1509203531184214067/nks3JtSmZgkb7qgH08_nxXYFBOrCiFs_9NxcAAcRTNbCxCvASPgdtEuR-DxtXG5-bc-U"

def cazar_fangames_fnaf():
    url = "https://itch.io/games/tag-fnaf.xml"
    
    print("🔦 Sincronizando radares con el feed Fazbear de Itch.io...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        respuesta = requests.get(url, headers=headers)
        
        if respuesta.status_code == 200:
            raiz = ET.fromstring(respuesta.content)
            items = raiz.findall('.//item')
            
            if not items:
                print("⚠️ El feed venía vacío.")
                return
                
            random.shuffle(items)
            embeds = []
            contador = 0
            ns = {'im': 'http://itch.io/rss'}
            
            for item in items:
                titulo = item.find('title').text if item.find('title') is not None else "Archivo Clasificado"
                url_juego = item.find('link').text if item.find('link') is not None else "https://itch.io"
                descripcion_raw = item.find('description').text if item.find('description') is not None else ""
                
                imagen_tag = item.find('im:image', ns)
                imagen_url = imagen_tag.text if imagen_tag is not None else None
                
                if descripcion_raw:
                    import re
                    descripcion = re.sub(r'<[^>]*>', '', descripcion_raw).strip()
                else:
                    descripcion = ""
                
                if not descripcion or len(descripcion) == 0:
                    descripcion = "No hay datos de transmisión. El archivo parece corrupto o encriptado por Fazbear Entertainment."
                    
                if len(descripcion) > 150:
                    descripcion = descripcion[:147] + "..."
                
                # 🛠️ DISEÑO PREMIUM ESTILO TERMINAL DE SEGURIDAD FNAF
                embed = {
                    "title": f"📝 {titulo.upper()}",
                    "url": url_juego,
                    "description": (
                        f"╔════════════════════════════════════╗\n"
                        f"   **SISTEMA DE MONITOREO AUTOMÁTICO**\n"
                        f"╚════════════════════════════════════╝\n\n"
                        f"⚠️ **REGISTRO DE ANOMALÍA:**\n"
                        f"*{descripcion}*\n\n"
                        f"📟 **Sujeto:** `Proyecto Comunitario`\n"
                        f"🔋 **Energía General:** `99%` 🟩\n"
                        f"📹 **Cámara Activa:** `CAM-08 (Itch.io)`\n"
                        f"──────────────────────────────────────"
                    ),
                    "color": 2818048, # Verde fósforo de monitor de seguridad viejo (Retro)
                    "image": {"url": imagen_url} if imagen_url else None,
                    "thumbnail": {
                        "url": "https://i.imgur.com/OcMRbT8.png" # Icono del monito de Freddy en pequeño arriba a la derecha
                    },
                    "footer": {
                        "text": "👁️ ARCHIVOS COMPROMETIDOS • NO APAGUES EL MONITOR",
                        "icon_url": "https://i.imgur.com/vH97Z9E.png"
                    }
                }
                
                embeds.append(embed)
                contador += 1
                if contador >= 2:
                    break
            
            if embeds:
                payload = {
                    "content": "🔴 ❗ **【 ENTRADA DE DATOS DETECTADA: UNIDAD GORDOBOT 】** ❗ 🔴\n*Alerta en los servidores. Se ha detectado código no autorizado en los monitores principales:*",
                    "embeds": embeds
                }
                requests.post(URL_DISCORD_FNAF, json=payload)
                print("¡Reporte Fazbear Estético enviado con éxito! 🐻🎉")
            else:
                print("⚠️ Error al estructurar las tarjetas.")
        else:
            print(f"❌ Error de conexión: {respuesta.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    cazar_fangames_fnaf()