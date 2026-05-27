import requests
import random
from datetime import datetime

# 📊 CONFIGURACIÓN DE TUS ENLACES:
URL_DISCORD_NOTICIAS = "https://discord.com/api/webhooks/1509192242563387455/V4hnU2XGCG8nt5YZUFAt7U6gUtaBq1eAawEL_w4w2o0WqE3rkPkah_XL7ozsTfdAKuhd"
API_KEY_NOTICIAS = "a3218623d03747de97b5e4b1643f1fd2"

def procesar_articulos(articulos, cantidad_deseada, etiqueta_por_defecto):
    """Filtra, limpia y desordena las noticias para que siempre sean diferentes"""
    # 🔀 ¡La magia! Barajamos la lista completa para que el orden sea al azar en cada ejecución
    random.shuffle(articulos)
    
    embeds_procesados = []
    contador = 0
    
    for art in articulos:
        titulo = art.get("title")
        descripcion = art.get("description")
        enlace = art.get("url")
        imagen = art.get("urlToImage")
        fuente = art.get("source", {}).get("name", etiqueta_por_defecto)
        autor = art.get("author", "Redacción")
        fecha_raw = art.get("publishedAt", "")
        
        # Filtros de calidad estricta
        if not titulo or not descripcion or "[Removed]" in titulo or "Removed" in descripcion:
            continue
            
        # Evitar duplicar noticias idénticas comparando títulos ya agregados
        if any(e["title"] == titulo for e in embeds_procesados):
            continue
            
        # Formatear la fecha de publicación
        try:
            fecha_objeto = datetime.strptime(fecha_raw, "%Y-%m-%dT%H:%M:%SZ")
            fecha_limpia = fecha_objeto.strftime("%d/%m/%Y")
        except:
            fecha_limpia = "Reciente"
            
        # Recortar textos para mantener la estética limpia de Discord
        if len(titulo) > 85:
            titulo = titulo[:82] + "..."
        if len(descripcion) > 160:
            descripcion = descripcion[:157] + "..."
        if "http" in autor or len(autor) > 25:
            autor = "Corresponsal"
            
        # Construcción estética del Embed individual
        embed = {
            "author": {
                "name": f"📰 {fuente.upper()}",
                "icon_url": "https://i.imgur.com/wSTFk6v.png"
            },
            "title": titulo,
            "url": enlace,
            "description": f"*{descripcion}*",
            "color": 2123412 if etiqueta_por_defecto == "Mundo" else 2067276, # Azul para internacional, Verde para México
            "image": {"url": imagen} if imagen else None,
            "fields": [
                {"name": "✍️ Autor", "value": f"`{autor}`", "inline": True},
                {"name": "📅 Publicado", "value": f"`{fecha_limpia}`", "inline": True}
            ],
            "footer": {
                "text": "🌐 GORDOBOT NEWS • COBERTURA AUTOMÁTICA 24/7",
                "icon_url": "https://i.imgur.com/OcMRbT8.png"
            }
        }
        
        embeds_procesados.append(embed)
        contador += 1
        if contador >= cantidad_deseada:
            break
            
    return embeds_procesados

def obtener_boletin_mixto():
    print("🛰️ Conectando con los satélites de noticias...")
    
    # 1. API Call para México (Buscamos notas locales en español)
    url_mx = f"https://newsapi.org/v2/everything?q=mexico&language=es&sortBy=relevancy&pageSize=30&apiKey={API_KEY_NOTICIAS}"
    
    # 2. API Call Internacional (Buscamos temas globales generales)
    url_int = f"https://newsapi.org/v2/everything?q=(mundo OR internacional OR global) -mexico&language=es&sortBy=popularity&pageSize=30&apiKey={API_KEY_NOTICIAS}"
    
    embeds_finales = []
    
    try:
        # Obtener y procesar las 2 de México
        res_mx = requests.get(url_mx)
        if res_mx.status_code == 200:
            articulos_mx = res_mx.json().get("articles", [])
            embeds_finales.extend(procesar_articulos(articulos_mx, 2, "México"))
            
        # Obtener y procesar las 3 Internacionales
        res_int = requests.get(url_int)
        if res_int.status_code == 200:
            articulos_int = res_int.json().get("articles", [])
            embeds_finales.extend(procesar_articulos(articulos_int, 3, "Mundo"))
            
        # Si logramos juntar noticias, las mandamos juntas en un solo paquete
        if embeds_finales:
            payload = {
                "content": "📡 ✨ **【 BOLETÍN GLOBAL E INTERNACIONAL INDEPENDIENTE 】** ✨ 📡\n*Reporte diario: 2 coberturas de México y 3 acontecimientos del resto del mundo.*",
                "embeds": embeds_finales
            }
            requests.post(URL_DISCORD_NOTICIAS, json=payload)
            print("¡Boletín mixto y aleatorio enviado con éxito! 🎉")
        else:
            print("⚠️ No se pudieron recopilar noticias válidas en esta tanda.")
            
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    obtener_boletin_mixto()