import requests
import random

# 🛍️ TU ENLACE DE DISCORD:
URL_MI_WEBHOOK = "https://discord.com/api/webhooks/1507247515869646901/H_vZBpFd1q6wpe1oeDWo_XQKOLjgzxM2_gpdNFv0hMior6EO_owMcL3s-BkCSjldMy_D"

def obtener_y_enviar_ofertas():
    # 🌟 CAMBIO CLAVE: Cambiamos el orden a 'Recent' (Ofertas nuevas) para asegurar que la lista mute constantemente
    url_mejores_ofertas = "https://www.cheapshark.com/api/1.0/deals?upperPrice=40&pageSize=150&sortBy=Recent"
    
    nombres_tiendas = {
        "1": "Steam", "25": "Epic Games Store", "7": "GOG", "3": "GreenManGaming", "11": "Humble Store"
    }
    
    print("🎲 Barajando un mazo gigante de ofertas frescas...")
    try:
        respuesta = requests.get(url_mejores_ofertas)
        if respuesta.status_code == 200:
            todas_las_ofertas = respuesta.json()
            
            # 🔀 ¡Mezclamos la lista completa ANTES de filtrar para romper el orden fijo de la API!
            random.shuffle(todas_las_ofertas)
            
            ofertas_filtradas = []
            juegos_agregados = set()
            
            for juego in todas_las_ofertas:
                # Si ya juntamos las 5 ofertas variadas que queríamos, nos detenemos
                if len(ofertas_filtradas) >= 5:
                    break
                    
                titulo = juego['title']
                ahorro = round(float(juego['savings']))
                
                # Filtro intermedio: Que tengan al menos un 25% de descuento real
                if ahorro >= 25 and titulo not in juegos_agregados:
                    juegos_agregados.add(titulo)
                    ofertas_filtradas.append(juego)
            
            # 🎨 Construimos las tarjetas estéticas (Embeds)
            embeds = []
            for juego in ofertas_filtradas:
                titulo = juego['title']
                precio_oferta = juego['salePrice']
                precio_normal = juego['normalPrice']
                ahorro = round(float(juego['savings']))
                id_tienda = juego['storeID']
                tienda = nombres_tiendas.get(id_tienda, "Otra tienda de PC")
                
                # Sacamos la foto del juego que nos da la API para que se vea INCREÍBLE
                imagen_juego = juego.get('thumb', '')
                
                embed = {
                    "title": f"🎮 {titulo}",
                    "color": 5763719,  # Verde gamer brillante
                    "thumbnail": {"url": imagen_juego},  # Añade la mini portada del juego a la derecha
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
                        "text": "Gordobot Ofertas • ¡Variedad Fresh Garantizada!"
                    }
                }
                embeds.append(embed)
            
            payload = {
                "content": "🔥 🏷️ **¡EL TOP 5 DE OFERTAZOS ALEATORIOS DEL DÍA!** 🏷️ 🔥\n*Lista fresca con rotación aleatoria de títulos.*",
                "embeds": embeds
            }
            
            if not embeds:
                payload = {"content": "❌ No se encontraron ofertas que superen los filtros en esta tanda."}
            
            requests.post(URL_MI_WEBHOOK, json=payload)
            print("¡Mensaje estético y ultra-variado enviado! 🎉")
        else:
            print(f"Error en la API: {respuesta.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    obtener_y_enviar_ofertas()