import requests
import time
import threading
from flask import Flask

# 🛍️ 1. PEGA TU URL DE DISCORD AQUÍ:
URL_MI_WEBHOOK = "https://discord.com/api/webhooks/1507235387787972618/z33xmXW_kTyrryuNnAXmyqIbaFhUZqeo_34EiWGvURlCKtI_VIYRSUXflXoSUM71gDd8"

app = Flask(__name__)

@app.route('/')
def home():
    return "El bot de ofertas optimizado está corriendo! 🚀"

def ciclo_bot():
    # Pedimos una lista más larga a la API (30 juegos) para tener de dónde elegir e ignorar repetidos
    url_mejores_ofertas = "https://www.cheapshark.com/api/1.0/deals?upperPrice=50&pageSize=30&sortBy=Metacritic"
    nombres_tiendas = {
        "1": "Steam", "25": "Epic Games Store", "7": "GOG", "3": "GreenManGaming", "11": "Humble Store"
    }
    
    while True:
        print("⏰ Iniciando el escaneo automático y filtrado de ofertas...")
        try:
            respuesta = requests.get(url_mejores_ofertas)
            if respuesta.status_code == 200:
                ofertas = respuesta.json()
                
                mensaje_discord = "🔥 🏷️ **¡EL TOP 5 DE OFERTAZOS DEL DÍA!** 🏷️ 🔥\n\n"
                
                juegos_agregados = set() # Aquí guardaremos los nombres para no repetirlos
                contador_top = 1
                
                for juego in ofertas:
                    # Si ya encontramos 5 juegos diferentes, dejamos de buscar
                    if contador_top > 5:
                        break
                        
                    titulo = juego['title']
                    precio_oferta = juego['salePrice']
                    precio_normal = juego['normalPrice']
                    ahorro = round(float(juego['savings']))
                    id_tienda = juego['storeID']
                    
                    # 🔍 FILTRO 1: Si el descuento es menor al 15%, lo ignoramos por completo
                    if ahorro < 15:
                        continue
                        
                    # 🔍 FILTRO 2: Si el juego ya está en nuestra lista, lo saltamos para no repetir
                    if titulo in juegos_agregados:
                        continue
                    
                    # Si pasó los filtros, lo guardamos en la lista de agregados
                    juegos_agregados.add(titulo)
                    tienda = nombres_tiendas.get(id_tienda, "Otra tienda de PC")
                    
                    # Construimos el renglón del juego
                    mensaje_discord += f"{contador_top}️⃣ **{titulo}**\n"
                    mensaje_discord += f"   🔹 Tienda: {tienda}\n"
                    mensaje_discord += f"   🔹 Descuento: ¡**{ahorro}% de DESCUENTO**!\n"
                    mensaje_discord += f"   🔹 Precio: ~~${precio_normal}~~ a **${precio_oferta} USD**\n\n"
                    
                    contador_top += 1
                
                # Si por alguna razón extraña de internet la lista quedó vacía
                if contador_top == 1:
                    mensaje_discord += "❌ Hoy no se encontraron ofertazos que superen los filtros de calidad."
                
                # Mandar a Discord
                datos_para_discord = {"content": mensaje_discord}
                requests.post(URL_MI_WEBHOOK, json=datos_para_discord)
                print("¡Ofertazos reales y variados enviados a Discord! 🎉")
            else:
                print(f"Error en la API: {respuesta.status_code}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        print("😴 Misión cumplida. El bot dormirá por 24 horas...")
        time.sleep(86400)

threading.Thread(target=ciclo_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)