import requests

# 🛍️ PEGA TU URL DE DISCORD AQUÍ:
URL_MI_WEBHOOK = "https://discord.com/api/webhooks/1507247515869646901/H_vZBpFd1q6wpe1oeDWo_XQKOLjgzxM2_gpdNFv0hMior6EO_owMcL3s-BkCSjldMy_D"

def enviar_ofertas():
    url_mejores_ofertas = "https://www.cheapshark.com/api/1.0/deals?upperPrice=50&pageSize=30&sortBy=Metacritic"
    nombres_tiendas = {
        "1": "Steam", "25": "Epic Games Store", "7": "GOG", "3": "GreenManGaming", "11": "Humble Store"
    }
    
    print("⏰ Iniciando el escaneo único de ofertas del día...")
    try:
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
                
                if ahorro < 15:
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
            
            # Enviar a Discord
            requests.post(URL_MI_WEBHOOK, json={"content": mensaje_discord})
            print("¡Ofertazos enviados con éxito! 🎉")
        else:
            print(f"Error en la API: {respuesta.status_code}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    enviar_ofertas()