import requests
import time
from datetime import datetime

# 🛍️ 1. AQUÍ VA TU ENLACE DE DISCORD (Asegúrate de poner tu webhook completo):
URL_MI_WEBHOOK = "https://discord.com/api/webhooks/1507247515869646901/H_vZBpFd1q6wpe1oeDWo_XQKOLjgzxM2_gpdNFv0hMior6EO_owMcL3s-BkCSjldMy_D" 

def obtener_y_enviar_ofertas():
    # 🌟 2. AQUÍ VA LA API DE JUEGOS (No la cambies por Discord):
    url_mejores_ofertas = "https://www.cheapshark.com/api/1.0/deals?upperPrice=50&pageSize=100&sortBy=Metacritic"
    
    nombres_tiendas = {
        "1": "Steam", "25": "Epic Games Store", "7": "GOG", "3": "GreenManGaming", "11": "Humble Store"
    }
    
    print("⏰ Ejecutando el escaneo diario de ofertas...")
    try:
        # Aquí el bot consulta a la API de juegos
        respuesta = requests.get(url_mejores_ofertas)
        if respuesta.status_code == 200:
            ofertas = respuesta.json()
            mensaje_discord = "🔥 🏷️ **¡EL TOP 5 DE OFERTAZOS DEL DÍA!** 🏷️ 🔥\n\n"
            
            juegos_agregados = set()
            contador_top = 1
            
            for juego in ofertas:
                if contador_top > 5:
                    break
                    
                titulo = juego['title']
                precio_oferta = juego['salePrice']
                precio_normal = juego['normalPrice']
                ahorro = round(float(juego['savings']))
                id_tienda = juego['storeID']
                
                if ahorro < 20:
                    continue
                    
                if titulo in juegos_agregados:
                    continue
                
                juegos_agregados.add(titulo)
                tienda = nombres_tiendas.get(id_tienda, "Otra tienda de PC")
                
                mensaje_discord += f"{contador_top}️⃣ **{titulo}**\n"
                mensaje_discord += f"   🔹 Tienda: {tienda}\n"
                mensaje_discord += f"   🔹 Descuento: ¡**{ahorro}% de DESCUENTO**!\n"
                mensaje_discord += f"   🔹 Precio: ~~${precio_normal}~~ a **${precio_oferta} USD**\n\n"
                
                contador_top += 1
            
            if contador_top == 1:
                mensaje_discord += "❌ Hoy no se encontraron ofertazos que superen los filtros de calidad."
            
            # Aquí el bot le manda el resultado final a tu Discord
            requests.post(URL_MI_WEBHOOK, json={"content": mensaje_discord})
            print("¡Mensaje diario enviado con éxito a Discord! 🎉")
        else:
            print(f"Error en la API de CheapShark: {respuesta.status_code}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    print("🚀 Alarma inteligente optimizada. Patrullando horarios críticos...")
    
    # Mandamos un reporte inicial inmediato para verificar que funcione
    obtener_y_enviar_ofertas()
    
    while True:
        ahora = datetime.now()
        
        # Alarma 1: 12:00 PM | Alarma 2: 08:00 PM
        if (ahora.hour == 12 and ahora.minute == 0) or (ahora.hour == 20 and ahora.minute == 0):
            print(f"⏰ ¡Hora crítica detectada ({ahora.hour}:00)! Buscando ofertas...")
            obtener_y_enviar_ofertas()
            time.sleep(65) 
        
        time.sleep(30)