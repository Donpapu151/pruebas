import requests
import random

# 🛍️ TU ENLACE DE DISCORD:
URL_MI_WEBHOOK = "https://discord.com/api/webhooks/1507247515869646901/H_vZBpFd1q6wpe1oeDWo_XQKOLjgzxM2_gpdNFv0hMior6EO_owMcL3s-BkCSjldMy_D"

def obtener_y_enviar_ofertas():
    # Pedimos una lista grande de 100 ofertas de calidad
    url_mejores_ofertas = "https://www.cheapshark.com/api/1.0/deals?upperPrice=50&pageSize=100&sortBy=Metacritic"
    nombres_tiendas = {
        "1": "Steam", "25": "Epic Games Store", "7": "GOG", "3": "GreenManGaming", "11": "Humble Store"
    }
    
    print("⏰ Buscando variedad de ofertas...")
    try:
        respuesta = requests.get(url_mejores_ofertas)
        if respuesta.status_code == 200:
            todas_las_ofertas = respuesta.json()
            
            # Filtramos primero para tener solo juegos de calidad con buen descuento
            ofertas_filtradas = []
            juegos_agregados = set()
            
            for juego in todas_las_ofertas:
                titulo = juego['title']
                ahorro = round(float(juego['savings']))
                
                # Filtro: Más de 20% de descuento y evitar repetidos
                if ahorro >= 20 and titulo not in juegos_agregados:
                    juegos_agregados.add(titulo)
                    ofertas_filtradas.append(juego)
            
            # 🎲 ¡Aquí está la magia de la variedad aleatoria!
            # Si hay más de 5 juegos válidos, tomamos 5 al azar de la lista
            if len(ofertas_filtradas) >= 5:
                ofertas_seleccionadas = random.sample(ofertas_filtradas, 5)
            else:
                ofertas_seleccionadas = ofertas_filtradas

            # 🎨 Creamos la estructura estética (Embeds) para Discord
            embeds = []
            
            for juego in ofertas_seleccionadas:
                titulo = juego['title']
                precio_oferta = juego['salePrice']
                precio_normal = juego['normalPrice']
                ahorro = round(float(juego['savings']))
                id_tienda = juego['storeID']
                tienda = nombres_tiendas.get(id_tienda, "Otra tienda de PC")
                
                # Diseñamos una tarjetita estética por cada juego
                embed = {
                    "title": f"🎮 {titulo}",
                    "color": 5763719,  # Un hermoso color verde gamer (en código HEX decimal)
                    "fields": [
                        {
                            "name": "🛍️ Tienda",
                            "value": tienda,
                            "inline": True
                        },
                        {
                            "name": "📉 Descuento",
                            "value": f"¡**{ahorro}% OFF**!",
                            "inline": True
                        },
                        {
                            "name": "💰 Precio Especial",
                            "value": f"~~${precio_normal}~~ a **${precio_oferta} USD**",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "Gordobot Ofertas • ¡Ahorra o nunca!"
                    }
                }
                embeds.append(embed)
            
            # Formato de envío final para Discord usando la lista de embeds
            payload = {
                "content": "🔥 🏷️ **¡EL TOP 5 DE OFERTAZOS ALEATORIOS DEL DÍA!** 🏷️ 🔥\n*Cada mensaje tiene variedad diferente para que no te pierdas de nada.*",
                "embeds": embeds
            }
            
            if not embeds:
                payload = {"content": "❌ Hoy no se encontraron ofertazos que superen los filtros de calidad."}
            
            requests.post(URL_MI_WEBHOOK, json=payload)
            print("¡Ofertazos variados y estéticos enviados con éxito! 🎉")
        else:
            print(f"Error en la API de CheapShark: {respuesta.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    obtener_y_enviar_ofertas()